import secrets
from datetime import timedelta

from django.shortcuts import render
from django.utils import timezone
from django.utils.timezone import now
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from Fitno import settings
from accounts.auth import CustomJWTAuthentication
from accounts.models import Customer, GymManager, OTP, User, APIKey
from accounts.permissions import IsGymManager, IsPlatformAdmin
from accounts.serializers import CustomerRegisterSerializer, PasswordLoginSerializer, GymManagerSerializer, \
    GymSerializer, UserRoleStatusSerializer, CustomerProfileSerializer, GymPanelCustomerListSerializer, \
    VerifyOTPSerializer, VerifyOTPResponseSerializer, RequestOTPSerializer, RequestOTPResponseSerializer, \
    AdminPanelCustomerDetailSerializer, GymPanelCustomerDetailSerializer
from gyms.models import Gym, MemberShip


# Create your views here.
# <=================== User Views ===================>
class UserRoleStatusView(generics.GenericAPIView):
    serializer_class = UserRoleStatusSerializer
    permission_classes = [AllowAny]  # می‌تونی بذاری IsAuthenticated اگه فقط برای لاگین‌ها بخوای

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            data = {
                "is_authenticated": True,
                "name": user.full_name,
                "is_customer": hasattr(user, "customer"),
                "is_gym_manager": hasattr(user, "gym_manager"),
                "is_platform_manager": hasattr(user, "platform_manager"),
            }
        else:
            data = {
                "is_authenticated": False,
                "name": None,
                "is_customer": False,
                "is_gym_manager": False,
                "is_platform_manager": False,
            }

        serializer = self.get_serializer(data)
        return Response(serializer.data)


class LogoutView(generics.GenericAPIView):
    """
    ویو لاگ اوت یک درخواست پست با بادی خالی
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token is None:
                return Response({"error": "Refresh token not found."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            response = Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
            # پاک کردن کوکی‌ها
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            return response

        except TokenError:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = PasswordLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        customer = user.customer

        # ساخت توکن‌ها
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response_data = {
            "user_id": user.id,
            "phone": user.phone,
            "full_name": user.full_name,
            "email": user.email,
            "national_code": customer.national_code,
            "city": customer.city,
            "refresh": refresh_token,
            "access": access_token,
        }

        response = Response(response_data, status=status.HTTP_200_OK)

        # ست کردن کوکی‌ها
        response.set_cookie(
            key=settings.SIMPLE_JWT["AUTH_COOKIE"],
            value=access_token,
            httponly=True,
            secure=settings.SIMPLE_JWT.get("AUTH_COOKIE_SECURE", False),
            samesite=settings.SIMPLE_JWT.get("AUTH_COOKIE_SAMESITE", "Lax"),
            max_age=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds(),
        )

        response.set_cookie(
            key=settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"],
            value=refresh_token,
            httponly=True,
            secure=settings.SIMPLE_JWT.get("AUTH_COOKIE_SECURE", False),
            samesite=settings.SIMPLE_JWT.get("AUTH_COOKIE_SAMESITE", "Lax"),
            max_age=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds(),
        )

        return response


class RequestOTPView(APIView):
    throttle_classes = [AnonRateThrottle]
    permission_classes = [AllowAny]

    @extend_schema(
        request=RequestOTPSerializer,
        responses={
            200: RequestOTPResponseSerializer,
            400: RequestOTPResponseSerializer,
            403: RequestOTPResponseSerializer,
            500: RequestOTPResponseSerializer
        },
        description="ارسال درخواست OTP با شماره موبایل"
    )
    def post(self, request):
        phone = request.data.get('phone')
        if not phone:
            return Response(
                {"error": "شماره موبایل الزامی است"},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.filter(phone=phone).first()
        if not user:
            return Response(
                {"error": "این شماره وجود ندارد"},
                status=status.HTTP_404_NOT_FOUND
            )
        OTP.objects.filter(user=user).delete()
        otp_code = str(secrets.randbelow(100000)).zfill(5)
        print(otp_code)
        expires_at = timezone.now() + timedelta(minutes=2)
        otp = OTP.objects.create(user=user, code=otp_code, expires_at=expires_at)
        success, message = otp.send_otp(phone=phone, otp_code=otp_code)
        if not success:
            return Response(
                {"error": f"خطا در ارسال OTP: {message}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(
            {"message": "لطفاً کد OTP را وارد کنید"},
            status=status.HTTP_200_OK
        )


class VerifyOTPView(APIView):
    throttle_classes = [AnonRateThrottle]
    permission_classes = [AllowAny]

    @extend_schema(
        request=VerifyOTPSerializer,
        responses={
            200: VerifyOTPResponseSerializer,
            400: VerifyOTPResponseSerializer,
            403: VerifyOTPResponseSerializer,
            404: VerifyOTPResponseSerializer
        },
        description="تأیید کد OTP و دریافت توکن‌های دسترسی"
    )
    def post(self, request):
        # (بقیه کد همونیه که فرستادی)
        api_key = request.headers.get('X-API-Key')
        if not api_key or not APIKey.objects.filter(key=api_key, is_active=True).exists():
            return Response(
                {"error": "Invalid API Key"},
                status=status.HTTP_403_FORBIDDEN
            )
        phone = request.data.get('phone')
        code = request.data.get('code')
        if not phone or not code:
            return Response(
                {"error": "Phone Parents and OTP code are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            otp = OTP.objects.filter(user=user).latest('created_at')
            if otp.code != code or not otp.is_valid():
                return Response(
                    {"error": "Invalid or expired OTP"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            otp.delete()
            if not user.is_active:
                user.is_active = True
                user.save()
        except OTP.DoesNotExist:
            return Response(
                {"error": "No OTP found"},
                status=status.HTTP_400_BAD_REQUEST
            )
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        response = Response(
            {"message": "Login successful"},
            status=status.HTTP_200_OK
        )
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            max_age=int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds())
        )
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            max_age=int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds())
        )
        return response


class RefreshTokenView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        if not refresh_token:
            return Response({"detail": "Refresh token not found in cookies"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh = RefreshToken(refresh_token)  # refresh_token از کوکی گرفته میشه
            access_token = str(refresh.access_token)  # فقط اکسس جدید ساخته میشه

            response = Response({
                "access": access_token
            }, status=status.HTTP_200_OK)

            # فقط اکسس توکن جدید تو کوکی ست میشه
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                value=access_token,
                httponly=True,
                secure=settings.SIMPLE_JWT.get('AUTH_COOKIE_SECURE', False),
                samesite=settings.SIMPLE_JWT.get('AUTH_COOKIE_SAMESITE', 'Lax'),
                max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
            )

            return response

        except Exception:
            return Response({"detail": "Invalid or expired refresh token"}, status=status.HTTP_401_UNAUTHORIZED)


# <=================== Customer Views ===================>
class CustomerRegisterView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response(
                {"detail": "شما قبلاً ثبت‌نام کرده‌اید و وارد شده‌اید."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()

        # توکن‌ها
        refresh = RefreshToken.for_user(customer.user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response_data = serializer.data
        response_data["access"] = access_token
        response_data["refresh"] = refresh_token

        response = Response(response_data, status=status.HTTP_201_CREATED)

        # ست کردن کوکی‌ها
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=access_token,
            httponly=True,
            secure=settings.SIMPLE_JWT.get('AUTH_COOKIE_SECURE', False),
            samesite=settings.SIMPLE_JWT.get('AUTH_COOKIE_SAMESITE', 'Lax'),
            max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
        )

        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            value=refresh_token,
            httponly=True,
            secure=settings.SIMPLE_JWT.get('AUTH_COOKIE_SECURE', False),
            samesite=settings.SIMPLE_JWT.get('AUTH_COOKIE_SAMESITE', 'Lax'),
            max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
        )

        return response


class CustomerProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        if hasattr(self.request.user, 'customer'):
            return self.request.user.customer


# <=================== GymManager Views ===================>
class GymManagerRegisterView(generics.CreateAPIView):
    queryset = GymManager.objects.all()
    serializer_class = GymManagerSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]


class FirstGymAddView(generics.CreateAPIView):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer
    permission_classes = [IsGymManager]
    authentication_classes = [CustomJWTAuthentication]


class GymPanelCustomerListView(generics.ListAPIView):
    serializer_class = GymPanelCustomerListSerializer
    permission_classes = [IsGymManager, IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'gym_secretary'):
            gym = user.gym_secretary.gym
            return Customer.objects.filter(memberships__gym=gym).distinct()

        elif hasattr(user, 'gym_manager'):
            gyms = user.gym_manager.gyms.all()
            return Customer.objects.filter(memberships__gym__in=gyms).distinct()

        return Customer.objects.none()


class GymPanelCustomerDetailView(generics.RetrieveAPIView):
    serializer_class = GymPanelCustomerDetailSerializer
    permission_classes = [IsGymManager]
    authentication_classes = [CustomJWTAuthentication]

    def get_queryset(self):
        user = self.request.user

        if hasattr(user, 'gym_secretary'):
            gym = user.gym_secretary.gym
            return Customer.objects.filter(memberships__gym=gym).distinct()

        elif hasattr(user, 'gym_manager'):
            gyms = user.gym_manager.gyms.all()
            return Customer.objects.filter(memberships__gym__in=gyms).distinct()

        return Customer.objects.none()


# <=================== Admin Views ===================>
class AdminPanelCustomerListView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = GymPanelCustomerListSerializer
    permission_classes = [IsPlatformAdmin]


class AdminPanelCustomerDetailView(generics.RetrieveDestroyAPIView):
    """
    نمایش جزئیات کامل مشتری شامل اطلاعات کاربری،
    اشتراک‌ها، ورود و خروج‌ها، باشگاه‌های بلاک‌شده و امتیازات
    """
    queryset = Customer.objects.select_related('user').prefetch_related(
        'memberships__gym', 'inouts__gym', 'blocked_gyms__gym', 'rates__gym'
    )
    serializer_class = AdminPanelCustomerDetailSerializer
    permission_classes = [IsPlatformAdmin]

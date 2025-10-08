from django.shortcuts import render
from django.utils.timezone import now
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from Fitno import settings
from accounts.auth import CustomJWTAuthentication
from accounts.models import Customer, GymManager
from accounts.permissions import IsGymManager
from accounts.serializers import CustomerRegisterSerializer, PasswordLoginSerializer, GymManagerSerializer, \
    GymSerializer, UserRoleStatusSerializer, CustomerProfileSerializer, GymPanelCustomerListSerializer
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

# 🔹 ثبت‌نام
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


# 🔹 پروفایل (GET + PATCH)
class CustomerProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        if hasattr(self.request.user, 'customer'):
            return self.request.user.customer


# <=================== GymManager Views ===================>
class GymManagerCreateView(generics.CreateAPIView):
    queryset = GymManager.objects.all()
    serializer_class = GymManagerSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]


class GymCreateView(generics.CreateAPIView):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer
    permission_classes = [IsGymManager]
    authentication_classes = [CustomJWTAuthentication]


class GymPanelCustomerListView(generics.ListAPIView):
    serializer_class = GymPanelCustomerListSerializer
    permission_classes = [IsGymManager, IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'gym_manager'):
            gym_manager = user.gym_manager

            active_memberships = MemberShip.objects.filter(
                gym__manager=gym_manager,
                is_active=True,
                end_date__gte=now().date()
            ).select_related('customer__user')

            customer_ids = active_memberships.values_list('customer_id', flat=True).distinct()
            return Customer.objects.filter(id__in=customer_ids).select_related('user')
        return Customer.objects.none()

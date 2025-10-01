from django.db.models import Q, Case, When, Value, IntegerField
from django.utils.timezone import now
from rest_framework import generics, status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.auth import CustomJWTAuthentication
from gyms.models import Gym, MemberShip, InOut
from gyms.serializers import CustomerPanelGymSerializer, CustomerPanelMembershipSerializer, \
    CustomerPanelInOutRequestSerializer, CustomerPanelGymSerializer


# Create your views here.
# <=================== Customer Views ===================>
class CustomerPanelGymList(generics.ListAPIView):
    serializer_class = CustomerPanelGymSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def get_queryset(self):
        customer = getattr(self.request.user, "customer", None)
        if not customer or not customer.gender:
            return Gym.objects.none()  # اگر جنسیت مشتری مشخص نبود

        return Gym.objects.filter(
            Q(gender="both") | Q(gender=customer.gender)
        )


class CustomerPanelGymDetail(generics.RetrieveAPIView):
    queryset = Gym.objects.filter(is_active=True)
    serializer_class = CustomerPanelGymSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]


class CustomerPanelCurrentGymList(generics.ListAPIView):
    serializer_class = CustomerPanelGymSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def get_queryset(self):
        customer = getattr(self.request.user, "customer", None)
        if not customer:
            return Gym.objects.none()
        return Gym.objects.filter(memberships__customer=customer, is_active=True).distinct()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            raise NotFound(detail="هیچ باشگاهی ثبت نام نشده است")
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_context(self):
        """برای دسترسی به request تو serializer"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class CustomerPanelCurrentGymDetail(generics.RetrieveAPIView):
    serializer_class = CustomerPanelGymSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        customer = getattr(self.request.user, "customer", None)
        if not customer:
            return Gym.objects.none()
        return Gym.objects.filter(memberships__customer=customer, is_active=True).distinct()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class CustomerPanelRequestGymEntry(generics.CreateAPIView):
    serializer_class = CustomerPanelInOutRequestSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def perform_create(self, serializer):
        user = self.request.user
        customer = getattr(user, "customer", None)
        if not customer:
            raise ValidationError("فقط مشتریان می‌توانند درخواست ورود بدهند.")

        gym_id = self.request.data.get("gym")
        if not gym_id:
            raise ValidationError("باشگاه الزامی است.")

        try:
            gym = Gym.objects.get(id=gym_id)
        except Gym.DoesNotExist:
            raise ValidationError("باشگاه مورد نظر یافت نشد.")

        # بررسی InOut باز
        if InOut.objects.filter(
                customer=customer,
                gym=gym
        ).filter(
            Q(confirm_in=False) |
            Q(enter_time__isnull=False, out_time__isnull=True)
        ).exists():
            raise ValidationError("شما یک درخواست ورود فعال دارید، تا زمان خروج نمی‌توانید درخواست جدید ثبت کنید.")

        # بررسی ممبرشیپ فعال
        membership = MemberShip.objects.filter(
            customer=customer,
            gym=gym,
            session_left__gt=0,
            validity_date__gte=now().date()
        ).first()

        if not membership:
            raise ValidationError("شما ممبرشیپ فعال برای این باشگاه ندارید.")

        # ساخت رکورد
        serializer.save(customer=customer, gym=gym, subscription=membership)


class CustomerMembershipListView(generics.ListAPIView):
    serializer_class = CustomerPanelMembershipSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def get_queryset(self):
        if hasattr(self.request.user, "customer"):
            customer = self.request.user.customer
            today = now().date()

            queryset = MemberShip.objects.filter(customer=customer)

            # Annotate با status عددی برای مرتب‌سازی
            queryset = queryset.annotate(
                is_active=Case(
                    When(session_left__gt=0, validity_date__gte=today, then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField()
                )
            ).order_by('-is_active', 'validity_date')

            return queryset


class CustomerMembershipSignUp(generics.CreateAPIView):
    """
    این یو ار ال برای ثبت نام در باشگاه و خرید سانس است
    بعد از اتصال درگاه پرداخت تکمیل میشود
     در حال حاضر صرفا برای سهولت توسعه گذاشته شده است
     """
    pass

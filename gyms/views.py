from django.db.models import Q, Case, When, Value, IntegerField
from django.utils.timezone import now
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.auth import CustomJWTAuthentication
from gyms.models import Gym, MemberShip
from gyms.serializers import CustomerPanelGymSerializer, CustomerPanelMembershipSerializer


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


class CustomerPanelCurrentGymDetail(generics.ListAPIView):
    serializer_class = CustomerPanelGymSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def get_queryset(self):
        customer = getattr(self.request.user, "customer", None)
        if not customer:
            return Gym.objects.none()
        return Gym.objects.filter(memberships__customer=customer).distinct()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            raise NotFound(detail="هیچ باشگاهی ثبت نام نشده است")
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomerMembershipListView(generics.ListAPIView):
    serializer_class = CustomerPanelMembershipSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def get_queryset(self):
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
        ).order_by('-is_active', 'validity_date')  # اول فعال‌ها، بعد غیر فعال‌ها؛ داخلش مرتب بر اساس تاریخ

        return queryset


class CustomerMembershipSignUp(generics.CreateAPIView):
    """
    این یو ار ال برای ثبت نام در باشگاه و خرید سانس است
    بعد از اتصال درگاه پرداخت تکمیل میشود
     در حال حاضر صرفا برای سهولت توسعه گذاشته شده است
     """
    pass

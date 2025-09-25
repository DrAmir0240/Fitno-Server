from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.auth import CustomJWTAuthentication
from accounts.models import Customer
from gyms.models import Gym
from gyms.serializers import CustomerPanelGymSerializer


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

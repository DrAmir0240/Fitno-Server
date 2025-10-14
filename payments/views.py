from django.contrib.contenttypes.models import ContentType
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import Http404

from accounts.models import User, PlatformSettings
from accounts.permissions import IsGymManager
from gyms.models import Gym, MemberShip
from payments.models import Transaction
from payments.serializers import CustomerPanelTransactionSerializer, GymPanelTransactionSerializer, \
    AdminPanelTransactionSerializer, AdminPanelInTransactionListSerializer, AdminPanelOutTransactionListSerializer, \
    AdminPanelCommissionTransactionListSerializer
from accounts.auth import CustomJWTAuthentication


# Create your views here.

# <=================== Customer Views ===================>
class CustomerPanelTransactionsListView(generics.ListAPIView):
    serializer_class = CustomerPanelTransactionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def get_queryset(self):
        return Transaction.objects.filter(payer=self.request.user).order_by('-id')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            raise Http404("تراکنشی برای این کاربر یافت نشد")
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# <=================== Gym Views ===================>
class GymPanelDepositTransactions(generics.ListAPIView):
    serializer_class = GymPanelTransactionSerializer
    permission_classes = [IsGymManager, IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        gyms = Gym.objects.filter(manager__user=user)
        memberships = MemberShip.objects.filter(gym__in=gyms)
        return Transaction.objects.filter(membership__in=memberships).distinct()


class GymPanelWithdrawalTransactions(generics.ListAPIView):
    serializer_class = GymPanelTransactionSerializer
    permission_classes = [IsGymManager, IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        gyms = Gym.objects.filter(manager__user=user)
        managers = [gym.manager.user for gym in gyms]
        return Transaction.objects.filter(receiver__in=managers).distinct()


# <=================== Admin Views ===================>
class AdminPanelInTransactionList(generics.ListAPIView):
    """
    لیست تراکنش های ورودی پلتفرم
    """
    serializer_class = AdminPanelInTransactionListSerializer

    def get_queryset(self):
        user_ct = ContentType.objects.get_for_model(User)
        customer_users = User.objects.filter(customer_profile__isnull=False)
        return Transaction.objects.filter(
            payer_content_type=user_ct,
            payer_object_id__in=customer_users.values_list('id', flat=True)
        ).order_by('-id')


class AdminPanelOutTransactionList(generics.ListAPIView):
    """
    لیست تراکنش های خروجی پلتفرم
    """
    serializer_class = AdminPanelOutTransactionListSerializer

    def get_queryset(self):
        platform_ct = ContentType.objects.get_for_model(PlatformSettings)
        user_ct = ContentType.objects.get_for_model(User)
        gym_manager_users = User.objects.filter(gym_manager_profile__isnull=False)
        return Transaction.objects.filter(
            payer_content_type=platform_ct,
            receiver_content_type=user_ct,
            receiver_object_id__in=gym_manager_users.values_list('id', flat=True)
        ).order_by('-id')


class AdminPanelCommissionTransactionList(generics.ListAPIView):
    """
    لیست کمیسیون های دریافتی(درآمد های خالص پلتفرم)
    """
    queryset = Transaction.objects.filter(is_commission=True).order_by('-id')
    serializer_class = AdminPanelCommissionTransactionListSerializer


class AdminPanelTransactionDetail(generics.RetrieveAPIView):
    """
    جزعیات تراکنش بر حسب ایدی تو هدر
    """
    queryset = Transaction.objects.all()
    serializer_class = AdminPanelTransactionSerializer

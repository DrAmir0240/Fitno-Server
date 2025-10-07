from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import Http404

from accounts.permissions import IsGymManager
from gyms.models import Gym, MemberShip
from payments.models import Transaction
from payments.serializers import CustomerPanelTransactionSerializer, TransactionSerializer
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
    serializer_class = TransactionSerializer
    permission_classes = [IsGymManager, IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        gyms = Gym.objects.filter(manager__user=user)
        memberships = MemberShip.objects.filter(gym__in=gyms)
        return Transaction.objects.filter(membership__in=memberships).distinct()


class GymPanelWithdrawalTransactions(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsGymManager, IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        gyms = Gym.objects.filter(manager__user=user)
        managers = [gym.manager.user for gym in gyms]
        return Transaction.objects.filter(receiver__in=managers).distinct()

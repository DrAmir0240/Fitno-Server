from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import Http404
from payments.models import Transaction
from payments.serializers import TransactionSerializer
from accounts.auth import CustomJWTAuthentication


# Create your views here.

# <=================== Customer Views ===================>
class CustomerPanelTransactionsListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
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

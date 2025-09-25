from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    payer_id = serializers.IntegerField(source="payer.id", read_only=True)
    payer_name = serializers.CharField(source="payer.full_name", read_only=True)
    receiver_id = serializers.IntegerField(source="receiver.id", read_only=True)
    receiver_name = serializers.CharField(source="receiver.full_name", read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id',
            'payer_id',
            'payer_name',
            'receiver_id',
            'receiver_name',
            'payment_method',
            'online_transaction',
            'price',
        ]

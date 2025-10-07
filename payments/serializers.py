from rest_framework import serializers
from .models import Transaction


# <=================== Customer Views ===================>
class CustomerPanelTransactionSerializer(serializers.ModelSerializer):
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


# <=================== Gym Views ===================>
class TransactionSerializer(serializers.ModelSerializer):
    membership = serializers.SerializerMethodField()
    payer_name = serializers.CharField(source='payer.full_name', read_only=True)
    receiver_name = serializers.CharField(source='receiver.full_name', read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'price', 'payment_method', 'online_transaction', 'payer_name', 'receiver_name', 'membership']

    def get_membership(self, obj):
        membership = getattr(obj, 'membership', None)
        if membership:
            return {
                "id": membership.id,
                "customer": membership.customer.user.full_name,
                "gym": membership.gym.title,
                "type": membership.type.title,
                "price": membership.price,
                "is_active": membership.is_active
            }
        return None

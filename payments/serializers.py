from rest_framework import serializers
from accounts.models import User, PlatformSettings
from payments.models import Transaction


# <=================== Customer Views ===================>
class CustomerPanelTransactionSerializer(serializers.ModelSerializer):
    payer_id = serializers.SerializerMethodField()
    payer_name = serializers.SerializerMethodField()
    receiver_id = serializers.SerializerMethodField()
    receiver_name = serializers.SerializerMethodField()

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

    # 🟢 متدهای پویا برای تشخیص مدل و برگرداندن فیلد مناسب
    def get_payer_id(self, obj):
        if obj.payer:
            return getattr(obj.payer, 'id', None)
        return None

    def get_payer_name(self, obj):
        if isinstance(obj.payer, User):
            return getattr(obj.payer, 'full_name', str(obj.payer))
        elif isinstance(obj.payer, PlatformSettings):
            return "پلتفرم فیتنو"
        return None

    def get_receiver_id(self, obj):
        if obj.receiver:
            return getattr(obj.receiver, 'id', None)
        return None

    def get_receiver_name(self, obj):
        if isinstance(obj.receiver, User):
            return getattr(obj.receiver, 'full_name', str(obj.receiver))
        elif isinstance(obj.receiver, PlatformSettings):
            return "پلتفرم فیتنو"
        return None


# <=================== Gym Views ===================>
class GymPanelTransactionSerializer(serializers.ModelSerializer):
    membership = serializers.SerializerMethodField()
    payer_name = serializers.SerializerMethodField()
    receiver_name = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = [
            'id',
            'price',
            'payment_method',
            'online_transaction',
            'payer_name',
            'receiver_name',
            'membership'
        ]

    # 🟢 نام پرداخت‌کننده
    def get_payer_name(self, obj):
        if isinstance(obj.payer, User):
            return getattr(obj.payer, 'full_name', str(obj.payer))
        elif isinstance(obj.payer, PlatformSettings):
            return "پلتفرم فیتنو"
        return None

    # 🟢 نام دریافت‌کننده
    def get_receiver_name(self, obj):
        if isinstance(obj.receiver, User):
            return getattr(obj.receiver, 'full_name', str(obj.receiver))
        elif isinstance(obj.receiver, PlatformSettings):
            return "پلتفرم فیتنو"
        return None

    # 🟢 اطلاعات عضویت (در صورت وجود)
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


# <=================== Admin Views ===================>
class AdminPanelInTransactionListSerializer(serializers.ModelSerializer):
    payer_name = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ['id', 'payer_name', 'price', 'created_at']

    def get_payer_name(self, obj):
        if isinstance(obj.payer, User):
            return getattr(obj.payer, 'full_name', str(obj.payer))
        elif isinstance(obj.payer, PlatformSettings):
            return "پلتفرم فیتنو"
        return "-"


class AdminPanelOutTransactionListSerializer(serializers.ModelSerializer):
    receiver_name = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ['id', 'receiver_name', 'price', 'created_at']

    def get_receiver_name(self, obj):
        if isinstance(obj.receiver, User):
            return getattr(obj.receiver, 'full_name', str(obj.receiver))
        elif isinstance(obj.receiver, PlatformSettings):
            return "پلتفرم فیتنو"
        return "-"


class AdminPanelCommissionTransactionListSerializer(serializers.ModelSerializer):
    payer_name = serializers.SerializerMethodField()
    gym_name = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ['id', 'gym_name', 'payer_name', 'price', 'created_at']

    def get_payer_name(self, obj):
        if isinstance(obj.payer, User):
            return getattr(obj.payer, 'full_name', str(obj.payer))
        return "-"

    def get_gym_name(self, obj):
        # فرض می‌کنیم Transaction → Membership با related_name='transaction' وصله
        membership = getattr(obj, 'membership', None)
        if membership and hasattr(membership, 'gym'):
            return membership.gym.title
        return "-"


class AdminPanelTransactionSerializer(serializers.ModelSerializer):
    payer_type = serializers.SerializerMethodField()
    payer_name = serializers.SerializerMethodField()
    receiver_type = serializers.SerializerMethodField()
    receiver_name = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = [
            'id',
            'price',
            'payment_method',
            'online_transaction',
            'is_commission',
            'payer_type',
            'payer_name',
            'receiver_type',
            'receiver_name',
        ]

    def get_payer_type(self, obj):
        return obj.payer_content_type.model if obj.payer_content_type else None

    def get_receiver_type(self, obj):
        return obj.receiver_content_type.model if obj.receiver_content_type else None

    def get_payer_name(self, obj):
        if isinstance(obj.payer, User):
            return getattr(obj.payer, 'full_name', str(obj.payer))
        elif isinstance(obj.payer, PlatformSettings):
            return "پلتفرم فیتنو"
        return None

    def get_receiver_name(self, obj):
        if isinstance(obj.receiver, User):
            return getattr(obj.receiver, 'full_name', str(obj.receiver))
        elif isinstance(obj.receiver, PlatformSettings):
            return "پلتفرم فیتنو"
        return None

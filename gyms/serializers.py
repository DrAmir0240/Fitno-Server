from django.utils.timezone import now
from rest_framework import serializers
from gyms.models import Gym, MemberShip, MemberShipType, InOut, GymImage, GymBanner


class CustomerPanelMemberShipTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberShipType
        fields = ['id', 'title', 'days', 'price']


class CustomerPanelMembershipSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    gym_title = serializers.CharField(source='gym.title', read_only=True)
    membership_type = serializers.CharField(source='type.name', read_only=True)

    class Meta:
        model = MemberShip
        fields = [
            'id',
            'gym_title',
            'membership_type',
            'start_date',
            'validity_date',
            'session_left',
            'price',
            'days',
            'status'
        ]

    def get_status(self, obj):
        from django.utils.timezone import now
        today = now().date()
        if obj.session_left > 0 and obj.validity_date and obj.validity_date >= today:
            return "فعال"
        return "غیرفعال"


class CustomerPanelInOutRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = InOut
        fields = ["id", "gym", "closet", "enter_time", "out_time", "confirm_in", "subscription"]
        read_only_fields = ["id", "enter_time", "out_time", "confirm_in", "subscription"]


class CustomerPanelGymImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymImage
        fields = ['id', 'image']


class CustomerPanelGymBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymBanner
        fields = ['id', 'banner', 'title', 'is_main']


class CustomerPanelMemberShipTypeForSignedGymSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberShipType
        fields = ['id', 'title', 'days', 'price', 'description']


class CustomerPanelMemberShipSerializer(serializers.ModelSerializer):
    gym_title = serializers.CharField(source='gym.title', read_only=True)
    type_title = serializers.CharField(source='type.title', read_only=True)

    class Meta:
        model = MemberShip
        fields = [
            'id', 'gym_title', 'type_title', 'start_date',
            'validity_date', 'session_left', 'price', 'days'
        ]


class CustomerPanelMemberShipCreateSerializer(serializers.ModelSerializer):
    membership_type_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MemberShip
        fields = [
            'id',
            'membership_type_id',
            'start_date',
            'validity_date',
            'session_left',
            'price',
            'days',
            'is_active',
        ]
        read_only_fields = ['start_date', 'validity_date', 'session_left', 'price', 'days', 'is_active']

    def create(self, validated_data):
        request = self.context['request']
        customer = request.user.customer  # فرض بر اینه که هر یوزر یک customer داره
        membership_type_id = validated_data.pop('membership_type_id')

        try:
            membership_type = MemberShipType.objects.get(id=membership_type_id)
        except MemberShipType.DoesNotExist:
            raise serializers.ValidationError({"membership_type_id": "Membership type not found."})

        from datetime import date, timedelta
        start_date = date.today()
        validity_date = start_date + timedelta(days=membership_type.days)

        membership = MemberShip.objects.create(
            customer=customer,
            gym=membership_type.gyms,
            type=membership_type,
            start_date=start_date,
            validity_date=validity_date,
            session_left=membership_type.days,
            price=membership_type.price,
            days=membership_type.days,
            transaction=None,
            is_active=False
        )
        return membership


class CustomerPanelGymSerializer(serializers.ModelSerializer):
    images = CustomerPanelGymImageSerializer(source='gymimage_set', many=True, read_only=True)
    banners = CustomerPanelGymBannerSerializer(source='gymbanner_set', many=True, read_only=True)
    membership_types = CustomerPanelMemberShipTypeForSignedGymSerializer(many=True, read_only=True)
    my_memberships = serializers.SerializerMethodField()

    class Meta:
        model = Gym
        fields = [
            'id', 'title', 'location', 'address', 'main_img',
            'phone', 'headline_phone', 'gender', 'commission_type',
            'facilities', 'description', 'work_hours_per_day', 'work_days_per_week',
            'images', 'banners', 'membership_types', 'my_memberships'
        ]

    def get_my_memberships(self, obj):
        """فقط ممبرشیپ‌هایی که مربوط به کاربر درخواست‌دهنده هستن"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return []
        customer = getattr(request.user, 'customer', None)
        if not customer:
            return []
        memberships = obj.memberships.filter(customer=customer)
        return CustomerPanelMemberShipSerializer(memberships, many=True).data

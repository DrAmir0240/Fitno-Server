from django.utils.timezone import now
from rest_framework import serializers
from gyms.models import Gym, MemberShip, MemberShipType, InOut, GymImage, GymBanner


class GymChoicesSerializer(serializers.Serializer):
    gyms = serializers.SerializerMethodField()
    gender_choices = serializers.SerializerMethodField()
    commission_type_choices = serializers.SerializerMethodField()

    def get_gyms(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return []
        gyms = Gym.objects.filter(manager__user=request.user)
        return [
            {"id": gym.id, "title": gym.title}
            for gym in gyms
        ]

    def get_gender_choices(self, obj):
        return [
            {"key": key, "value": value}
            for key, value in Gym._meta.get_field('gender').choices
        ]

    def get_commission_type_choices(self, obj):
        return [
            {"key": key, "value": value}
            for key, value in Gym._meta.get_field('commission_type').choices
        ]


# <=================== Customer Views ===================>
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


class CustomerPanelSignedGymListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = ['id', 'title', 'main_img']


class CustomerPanelGymSerializer(serializers.ModelSerializer):
    images = CustomerPanelGymImageSerializer(source='gymimage_set', many=True, read_only=True)
    banners = CustomerPanelGymBannerSerializer(source='gymbanner_set', many=True, read_only=True)
    membership_types = CustomerPanelMemberShipTypeForSignedGymSerializer(many=True, read_only=True)
    my_memberships = serializers.SerializerMethodField()

    class Meta:
        model = Gym
        fields = [
            'id', 'title', 'location', 'address', 'main_img',
            'phone', 'headline_phone', 'gender',
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


class CustomerPanelInOutSerializer(serializers.ModelSerializer):
    gym = serializers.SlugRelatedField(read_only=True, slug_field='title')
    subscription = serializers.SerializerMethodField()

    class Meta:
        model = InOut
        fields = ['gym', 'closet', 'enter_time', 'out_time', 'subscription']

    def get_subscription(self, obj):
        return obj.subscription


# <=================== Gym Views ===================>
class GymPanelGymImageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = GymImage
        fields = ['id', 'image']


class GymPanelGymSerializer(serializers.ModelSerializer):
    images = GymPanelGymImageSerializer(source='gymimage_set', many=True, required=False)

    class Meta:
        model = Gym
        fields = [
            'id', 'title', 'location', 'address', 'main_img', 'phone',
            'headline_phone', 'gender', 'commission_type', 'facilities',
            'description', 'work_hours_per_day', 'work_days_per_week',
            'is_active', 'images'
        ]
        read_only_fields = ['is_active']

    def create(self, validated_data):
        """
        هنگام ساخت Gym جدید:
        - manager از یوزر درخواست استخراج میشه.
        - is_active همیشه False ست میشه.
        - در صورت وجود تصاویر، آن‌ها نیز ساخته می‌شن.
        """
        request = self.context.get('request')
        manager = getattr(request.user, 'gym_manager', None)

        if manager is None:
            raise serializers.ValidationError("مدیر معتبر یافت نشد.")

        images_data = validated_data.pop('gymimage_set', [])

        # ایجاد Gym جدید
        gym = Gym.objects.create(manager=manager, is_active=False, **validated_data)

        # افزودن تصاویر در صورت وجود
        for img_data in images_data:
            GymImage.objects.create(gym=gym, **img_data)

        return gym

    def update(self, instance, validated_data):
        images_data = validated_data.pop('gymimage_set', [])

        # update main gym fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # handle images
        existing_images = {img.id: img for img in instance.gymimage_set.all()}

        for img_data in images_data:
            img_id = img_data.get('id', None)
            if img_id and img_id in existing_images:
                # Update existing image
                existing_images[img_id].image = img_data.get('image', existing_images[img_id].image)
                existing_images[img_id].save()
                existing_images.pop(img_id)
            else:
                # Create new image
                GymImage.objects.create(gym=instance, **img_data)

        # Delete removed images
        for remaining_img in existing_images.values():
            remaining_img.delete()

        return instance


class GymPanelMemberShipTypeSerializer(serializers.ModelSerializer):
    gym_title = serializers.CharField(source='gyms.title', read_only=True)

    class Meta:
        model = MemberShipType
        fields = ['id', 'title', 'gym_title', 'gyms', 'days', 'price', 'description']

    def validate_gyms(self, value):
        """
        بررسی کنه gym انتخاب‌شده واقعاً متعلق به مدیر لاگین‌شده هست
        """
        request = self.context.get('request')
        user = request.user
        if not hasattr(user, 'gym_manager'):
            raise serializers.ValidationError("مدیر معتبر یافت نشد.")
        if value.manager != user.gym_manager:
            raise serializers.ValidationError("شما اجازه افزودن عضویت برای این باشگاه را ندارید.")
        return value


class GymPanelGymBannerSerializer(serializers.ModelSerializer):
    gym_title = serializers.CharField(source='gym.title', read_only=True)

    class Meta:
        model = GymBanner
        fields = ['id', 'title', 'banner', 'is_main', 'gym', 'gym_title']
        read_only_fields = ['is_main']

    def validate_gym(self, value):
        """
        فقط اجازه بده برای باشگاه‌های متعلق به یوزر فعلی بنر ساخته بشه
        """
        request = self.context.get('request')
        user = request.user

        if not hasattr(user, 'gym_manager'):
            raise serializers.ValidationError("مدیر معتبر یافت نشد.")
        if value.manager != user.gym_manager:
            raise serializers.ValidationError("شما اجازه افزودن بنر برای این باشگاه را ندارید.")

        return value


# <=================== Admin Views ===================>
class AdminPanelGymListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = ['id', 'title', 'main_img']

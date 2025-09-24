from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import Customer, User, GymManager
from gyms.models import Gym


class CustomerRegisterSerializer(serializers.ModelSerializer):
    # فیلدهای یوزر
    phone = serializers.CharField(max_length=11, write_only=True)
    full_name = serializers.CharField(max_length=255, write_only=True)
    email = serializers.EmailField(required=False, allow_blank=True, allow_null=True, write_only=True)
    password = serializers.CharField(write_only=True, min_length=6)

    # فیلدهای مشتری
    national_code = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
    city = serializers.CharField(max_length=255, write_only=True)

    # توکن‌ها
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    class Meta:
        model = Customer
        fields = [
            'phone', 'full_name', 'email', 'password',
            'national_code', 'city',
            'access', 'refresh'
        ]

    def create(self, validated_data):
        phone = validated_data.pop('phone')
        full_name = validated_data.pop('full_name')
        email = validated_data.pop('email', None)
        password = validated_data.pop('password')
        national_code = validated_data.pop('national_code', None)
        city = validated_data.pop('city')

        # ساخت یوزر
        user = User.objects.create(
            phone=phone,
            full_name=full_name,
            email=email
        )
        user.set_password(password)
        user.save()

        # ساخت مشتری
        customer = Customer.objects.create(
            user=user,
            national_code=national_code,
            city=city
        )
        return customer

    def to_representation(self, instance):
        """
        خروجی نهایی شامل همه‌ی داده‌های Customer + User + توکن‌ها
        """
        data = super().to_representation(instance)

        # اطلاعات یوزر
        data['user_id'] = instance.user.id
        data['phone'] = instance.user.phone
        data['full_name'] = instance.user.full_name
        data['email'] = instance.user.email

        # اطلاعات مشتری
        data['national_code'] = instance.national_code
        data['city'] = instance.city

        # توکن‌ها
        refresh = RefreshToken.for_user(instance.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data


class CustomerLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        phone = attrs.get("phone")
        password = attrs.get("password")

        user = authenticate(phone=phone, password=password)
        if not user:
            raise serializers.ValidationError("شماره یا پسورد اشتباه است.")

        if not hasattr(user, "customer"):
            raise serializers.ValidationError("این کاربر مشتری نیست.")

        attrs["user"] = user
        return attrs


class GymManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymManager
        fields = ['id', 'national_code', 'verification_code', 'balance', 'city', 'invitation_code']
        read_only_fields = ['id', 'balance']

    def create(self, validated_data):
        # یوزر از کانتکست گرفته میشه
        user = self.context['request'].user
        return GymManager.objects.create(user=user, **validated_data)


class GymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = [
            'id', 'title', 'location', 'address', 'main_img',
            'phone', 'headline_phone', 'commission_type',
            'facilities', 'description', 'work_hours_per_day', 'work_days_per_week'
        ]
        read_only_fields = ['id', 'manager']

    def create(self, validated_data):
        # مدیر از یوزر لاگین گرفته میشه
        user = self.context['request'].user
        gym_manager = getattr(user, 'gym_manager', None)
        if not gym_manager:
            raise serializers.ValidationError("این کاربر مدیر باشگاه نیست.")
        return Gym.objects.create(manager=gym_manager, **validated_data)

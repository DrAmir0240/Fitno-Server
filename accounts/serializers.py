from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import Customer, User, GymManager
from gyms.models import Gym


class UserRoleStatusSerializer(serializers.Serializer):
    is_authenticated = serializers.BooleanField()
    name = serializers.CharField(allow_null=True)
    is_customer = serializers.BooleanField()
    is_gym_manager = serializers.BooleanField()
    is_platform_manager = serializers.BooleanField()


class CustomerRegisterSerializer(serializers.ModelSerializer):
    # فیلدهای یوزر
    phone = serializers.CharField(max_length=11, write_only=True)
    full_name = serializers.CharField(max_length=255, write_only=True)
    email = serializers.EmailField(required=False, allow_blank=True, allow_null=True, write_only=True)
    password = serializers.CharField(write_only=True, min_length=6)

    # فیلدهای مشتری
    national_code = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
    city = serializers.CharField(max_length=255, write_only=True)
    profile_photo = serializers.ImageField(required=False, allow_null=True)
    gender = serializers.ChoiceField(choices=(('male', 'مرد'), ('female', 'زن')), default='male')

    # توکن‌ها
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    class Meta:
        model = Customer
        fields = [
            'phone', 'full_name', 'email', 'password',
            'national_code', 'city', 'profile_photo', 'gender',
            'access', 'refresh'
        ]

    def create(self, validated_data):
        phone = validated_data.pop('phone')
        full_name = validated_data.pop('full_name')
        email = validated_data.pop('email', None)
        password = validated_data.pop('password')
        national_code = validated_data.pop('national_code', None)
        city = validated_data.pop('city')
        profile_photo = validated_data.pop('profile_photo', None)
        gender = validated_data.pop('gender', 'male')

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
            city=city,
            profile_photo=profile_photo,
            gender=gender
        )
        return customer

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # اطلاعات یوزر
        data['user_id'] = instance.user.id
        data['phone'] = instance.user.phone
        data['full_name'] = instance.user.full_name
        data['email'] = instance.user.email

        # اطلاعات مشتری
        data['national_code'] = instance.national_code
        data['city'] = instance.city
        data['gender'] = instance.gender
        data['profile_photo'] = instance.profile_photo.url if instance.profile_photo else None

        # توکن‌ها
        refresh = RefreshToken.for_user(instance.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data


class CustomerProfileSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source="user.phone", read_only=True)  # غیرقابل تغییر
    email = serializers.EmailField(source="user.email", read_only=True)  # غیرقابل تغییر
    full_name = serializers.CharField(source="user.full_name", required=False)

    class Meta:
        model = Customer
        fields = [
            'id', 'phone', 'email', 'full_name',
            'national_code', 'city', 'gender', 'profile_photo'
        ]

    def update(self, instance, validated_data):
        # آپدیت Customer
        instance.national_code = validated_data.get("national_code", instance.national_code)
        instance.city = validated_data.get("city", instance.city)
        instance.gender = validated_data.get("gender", instance.gender)

        if "profile_photo" in validated_data:
            instance.profile_photo = validated_data.get("profile_photo", instance.profile_photo)

        instance.save()

        # آپدیت full_name در User (اجازه داریم تغییر بدیم)
        user_data = validated_data.get("user", {})
        if "full_name" in user_data:
            instance.user.full_name = user_data["full_name"]
            instance.user.save()

        return instance


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

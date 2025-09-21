import secrets

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from accounts.managers import CustomUserManager


# Create your models here.
class APIKey(models.Model):
    key = models.CharField(max_length=5000, unique=True)
    client_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client_name} - {self.key[:10]}..."

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = secrets.token_urlsafe(52)[:70]  # تولید رشته رندوم 70 کاراکتری
        super().save(*args, **kwargs)


class PlatformSettings(models.Model):
    # This table is intended to have exactly one row.
    commission_for_club_per_month = models.IntegerField(default=0)
    commission_for_club_per_day = models.IntegerField(default=0)
    commission_for_marketer = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    announcements = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk and PlatformSettings.objects.exists():
            raise ValueError('Only one PlatformSettings instance is allowed')
        return super().save(*args, **kwargs)

    def __str__(self):
        return 'Platform Settings'


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=11, unique=True, verbose_name="phone")
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.phone


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    national_code = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.user.full_name


class PlatformManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='platform_manager')
    access_code = models.CharField(max_length=100)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.user.full_name


class GymManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='gym_manager')
    national_code = models.CharField(max_length=50, blank=True, null=True)
    verification_code = models.CharField(max_length=100, blank=True, null=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    city = models.CharField(max_length=255, blank=True, null=True)
    invitation_code = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.full_name

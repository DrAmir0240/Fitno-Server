from django.db import models
from django.db.models import Q

from accounts.models import Customer, GymManager
from payments.models import Transaction


# Create your models here.
class Gym(models.Model):
    title = models.CharField(max_length=255)
    manager = models.ForeignKey(GymManager, on_delete=models.CASCADE, related_name='gyms')
    location = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField()
    main_img = models.ImageField(upload_to='gym_img/main_imgs')
    phone = models.CharField(max_length=50)
    headline_phone = models.CharField(max_length=50)
    gender = models.CharField(max_length=50,
                              choices=(('both', 'زنانه و مردانه'), ('female', 'زنانه'), ('male', 'مردانه')),
                              default='male')
    commission_type = models.CharField(max_length=50, choices=(
        ('customer', 'مشتری'),
        ('gym', 'باشگاه')
    ))
    facilities = models.CharField(max_length=5000)
    description = models.TextField()
    work_hours_per_day = models.CharField(max_length=500)
    work_days_per_week = models.CharField(max_length=500)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class GymImage(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gym_img/gym_img')

    def __str__(self):
        return self.gym.title + ':' + str(self.id)


class GymBanner(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    banner = models.ImageField(upload_to='gym_img/banner_img')
    is_main = models.BooleanField(default=False)
    title = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['gym'],
                condition=Q(is_main=True),
                name='unique_main_banner_per_gym'
            )
        ]

    def __str__(self):
        return self.title + " for:" + self.gym.title


class MemberShipType(models.Model):
    title = models.CharField(max_length=255)
    gyms = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='membership_types')
    days = models.IntegerField(default=0)
    type = models.CharField(max_length=255, choices=(('daily', 'روزانه'), ('monthly', 'ماهانه')), default='monthly')
    price = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title + " for: " + self.gyms.title


class MemberShip(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='memberships')
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='memberships')
    type = models.ForeignKey(MemberShipType, on_delete=models.CASCADE, related_name='memberships')
    start_date = models.DateField(null=True, blank=True)
    validity_date = models.DateField(null=True, blank=True)
    session_left = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transaction = models.OneToOneField(Transaction, on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name='membership')
    days = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"Membership {self.customer.user.full_name} - {self.gym.title}"


class Closet(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='closets')
    number = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=(("available", "در دسترس"), ("unavailable", "غیرقابل دسترس")),
                              default='available')

    def __str__(self):
        return f"{self.gym.title} - {self.number}"


class InOut(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='inouts')
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='inouts')
    closet = models.ForeignKey(Closet, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    enter_time = models.DateTimeField(null=True, blank=True)
    out_time = models.DateTimeField(null=True, blank=True)
    confirm_in = models.BooleanField(default=False)
    subscription = models.ForeignKey(MemberShip, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='+')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"InOut {self.customer} @ {self.gym}"


class BlockList(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='blocked_gyms')
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='blocked_by')
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} blocked {self.gym}"


class Rate(models.Model):
    rate = models.PositiveSmallIntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='rates')
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='rates')

    def __str__(self):
        return f"{self.rate} by {self.customer} for {self.gym}"

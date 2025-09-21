from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, full_name, password=None, **extra_fields):
        if not phone:
            raise ValueError("شماره تلفن باید وارد شود")

        if not full_name:
            raise ValueError("نام کامل کاربر باید وارد شود")  # ← اجباری کردن full_name

        if not password:
            raise ValueError("کاربر باید پسورد داشته باشد")  # ← اجباری کردن پسورد

        user = self.model(phone=phone, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_deleted', False)
        extra_fields.setdefault('is_active', True)

        if not full_name:
            raise ValueError("نام کامل سوپر یوزر باید وارد شود")

        if not password:
            raise ValueError("سوپریوزر باید پسورد داشته باشد")

        return self.create_user(phone, full_name, password, **extra_fields)

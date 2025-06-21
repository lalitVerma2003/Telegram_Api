from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from utils.common_models import common_model

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, common_model):
    fullname = models.CharField(max_length=255,null=True,blank=True)
    email = models.EmailField(unique=True ,null=True,blank=True)
    phone_no = models.CharField(max_length=20,null=True,blank=True, unique=True)
    country_code = models.CharField(max_length=20,null=True,blank=True)
    profile_pic_url = models.TextField(blank=True, null=True)
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["fullname", "phone_no"]

    class Meta:
        db_table = "users"
        ordering = ["-created_at"]


class DEVICE_CHOICES(models.TextChoices):
    MOBILE = "mobile", "Mobile"
    TABLET = "tablet", "Tablet"
    DESKTOP = "desktop", "Desktop"


class OS_CHOICES(models.TextChoices):
    ANDROID = "android", "Android"
    IOS = "ios", "iOS"
    WINDOWS = "windows", "Windows"
    LINUX = "linux", "Linux"


class UserDevice(common_model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    device_id = models.CharField(max_length=255, blank=True, null=True)
    device_type = models.CharField(choices=DEVICE_CHOICES, default="mobile")
    device_token = models.CharField(max_length=255, blank=True, null=True)
    os = models.CharField(choices=OS_CHOICES, default="android")

    class Meta:
        db_table = "user_device"
        ordering = ["-created_at"]
        unique_together = ("user_id", "device_id")


class Sessions(common_model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    user_device_id = models.ForeignKey(
        UserDevice, on_delete=models.CASCADE, db_column="device_id", null=True
    )
    access_token = models.TextField()
    refresh_token = models.TextField()

    class Meta:
        db_table = "users_sessions"
        ordering = ["-created_at"]
import uuid

from PIL import Image
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import CustomUserManager


# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    image = models.ImageField(default='default-avatar.png', upload_to='profile_pics')
    date_joined = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name.capitalize()} {self.last_name.capitalize()}'
        return self.username

    def get_short_name(self):
        if self.first_name:
            return self.first_name.capitalize()
        return self.username

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 250 or img.width > 250:
            img.thumbnail((250, 250))
            img.save(self.image.path)

    def __str__(self):
        return self.username


class OTP(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=8)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()
    u_link = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return f"{self.user.username}'s OTP"

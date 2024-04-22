from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomUser
from .utils import send_otp_email


@receiver(post_save, sender=CustomUser)
def create_and_send_otp(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        send_otp_email(instance)

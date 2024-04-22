from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.crypto import get_random_string

from .models import OTP


def delete_expired_otps():
    OTP.objects.filter(expires_at__lt=timezone.now()).delete()


def send_otp_email(user):
    otp = get_random_string(length=8)
    expire_duration = settings.OTP_EXPIRE_DURATION
    expires_at = timezone.now() + timezone.timedelta(minutes=expire_duration)
    otp_obj = OTP.objects.create(user=user, otp=otp, expires_at=expires_at)
    user.is_active = False
    user.save()
    base_url = settings.BASE_URL if hasattr(settings, 'BASE_URL') else 'http://localhost:8000'
    subject = "Verify Your Email Address"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    message = f"""
        Hi {user.username},

        Thank you for signing up for my Website!

        To complete your registration and activate your account, enter the One-Time Password (OTP) in the Verification link given below:
        Remember, This OTP and the Verification link is valid for {expire_duration} minutes only. Hurry UP!

        OTP: {otp}

        Verification Link: {base_url}/verify-email/{user.username}/{otp_obj.u_link}/
        
        OTP expires at: {expires_at.strftime("%B %d, %Y, at %I:%M:%S %p")}
        """
    send_mail(subject, message, from_email, recipient_list)
    delete_expired_otps()

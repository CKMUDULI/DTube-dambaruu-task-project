from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, Form


class CustomUserUpdateForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'image',)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password1', 'password2')


class EmailVerificationForm(Form):
    otp = forms.CharField(label='OTP', max_length=8)


class ResendOTPForm(Form):
    email = forms.EmailField(label='Email')

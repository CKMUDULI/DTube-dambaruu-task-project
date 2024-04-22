from django.contrib import messages
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import UpdateView, ListView

from videos.models import VideoPost
from .forms import CustomUserUpdateForm, CustomUserCreationForm, EmailVerificationForm, ResendOTPForm
from .models import CustomUser, OTP
from .utils import send_otp_email


class UserLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'users/login.html'
    success_url = reverse_lazy('users:profile')

    def post(self, request, *args, **kwargs):
        email = self.request.POST.get('username')
        password = self.request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(self.request, 'You are now logged in.')
                return redirect('users:profile')
            else:
                try:
                    otp_obj = OTP.objects.get(user=user, expires_at__gte=timezone.now())
                    messages.warning(request, 'Please check your email and enter your OTP to activate your account.')
                    return redirect(
                        reverse('users:verify-email', kwargs={'username': user.username, 'u_link': otp_obj.u_link}))
                except OTP.DoesNotExist:
                    messages.warning(self.request,
                                     'Your account is not active. Please verify your email and try again.')
                    return redirect('users:resend-otp')
        messages.error(self.request, 'Invalid email or password.')
        return redirect('users:login')


class UserProfileView(LoginRequiredMixin, ListView):
    template_name = 'users/index.html'
    context_object_name = 'videos'
    extra_context = {'section': 'my_videos'}
    paginate_by = 5
    paginate_orphans = 1

    def get_queryset(self):
        user = get_object_or_404(CustomUser, pk=self.request.user.pk)
        return VideoPost.objects.filter(author=user)


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = CustomUserUpdateForm
    template_name = 'users/update_profile.html'
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        messages.info(self.request, 'Your profile has been updated!')
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return self.request.user


class UserLogoutView(LogoutView):
    template_name = 'users/logout.html'


def user_signup(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already a logged in user.')
        return redirect('users:profile')
    # form = CustomUserCreationForm(request.POST or None)
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            u_link = OTP.objects.filter(user=user).first().u_link
            messages.success(request, "Account created successfully! An OTP was sent to your Email")
            return redirect('users:verify-email', username=user.username, u_link=u_link)
    return render(request, 'users/signup.html', {'form': form})


def verify_email(request, username, u_link):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already a logged in user.')
        return redirect('users:profile')
    user = get_object_or_404(CustomUser, username=username)
    user_otp = get_object_or_404(OTP, user=user, u_link=u_link)
    if request.method == 'POST':
        if user_otp.otp == request.POST.get('otp'):
            if user_otp.expires_at > timezone.now():
                user.is_active = True
                user.save()
                user_otp.delete()
                messages.success(request, 'Your account has been verified! You can login now.')
                return redirect('users:login')
            else:
                user_otp.delete()
                messages.warning(request, 'Your OTP has been expired! Request a new OTP.')
                return redirect('users:resend-otp')
        else:
            u_link = OTP.objects.filter(user=user).first().u_link
            messages.error(request, 'Invalid OTP!')
            return redirect('users:verify-email', username=user.username, u_link=u_link)
    if user_otp.expires_at < timezone.now():
        user_otp.delete()
        messages.warning(request, 'Your OTP has been expired! Request a new OTP.')
        return redirect('users:resend-otp')
    return render(request, 'users/verify.html', {'form': EmailVerificationForm()})


def resend_otp(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already a logged in user.')
        return redirect('users:profile')
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.warning(request, 'Email does not exist on server. Enter a valid email.')
            return redirect('users:resend-otp')
        if user.is_active:
            messages.warning(request, 'Your account is already activated.')
            return redirect('users:login')
        OTP.objects.filter(user=user).delete()
        send_otp_email(user)
        u_link = OTP.objects.filter(user=user).first().u_link
        messages.success(request, 'Your OTP has been sent to your Email')
        return redirect('users:verify-email', username=user.username, u_link=u_link)
    return render(request, 'users/resend_otp.html', {'form': ResendOTPForm()})

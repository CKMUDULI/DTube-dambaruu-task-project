from django.urls import path, include

from .views import UserLoginView, UserProfileView, UserLogoutView, UserProfileUpdateView, user_signup, verify_email, \
    resend_otp

app_name = 'users'
urlpatterns = [
    path('', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('index/', UserProfileView.as_view(), name='profile'),
    path('update-profile/', UserProfileUpdateView.as_view(), name='update-profile'),
    path('signup/', user_signup, name='signup'),
    path("verify-email/<slug:username>/<uuid:u_link>/", verify_email, name="verify-email"),
    path("resend-otp/", resend_otp, name="resend-otp"),
    path('videos/', include('videos.urls', namespace='videos')),
]

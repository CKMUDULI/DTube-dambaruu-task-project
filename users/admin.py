from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, OTP

# Register your models here.
admin.site.register(OTP)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_superuser', 'is_staff')
    list_filter = ('is_superuser', 'is_staff')
    search_fields = ('username', 'email')
    fieldsets = (
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["first_name", "last_name", "username", "image"]}),
        ("Permissions", {"fields": ["is_active", "is_staff", "is_superuser", "groups", "user_permissions"]}),
        ("Important dates", {"fields": ["last_login", "date_joined"]}),
    )
    add_fieldsets = (
        (None, {"fields": ["email", "username", "password1", "password2"]}),
    )

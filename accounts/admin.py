from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'full_name', 'role', 'is_active')
    list_filter = ('role', 'is_active', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('اطلاعات تکمیلی', {
            'fields': ('full_name', 'phone', 'avatar', 'role', 'gender',
                       'bio', 'birth_date', 'city', 'country', 'website', 'interest')
        }),
    )
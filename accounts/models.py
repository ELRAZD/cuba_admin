from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', _('مدیر')),
        ('manager', _('مدیر میانی')),
        ('user', _('کاربر عادی')),
    )
    GENDER_CHOICES = (
        ('male', _('مرد')),
        ('female', _('زن')),
        ('other', _('سایر')),
    )

    full_name = models.CharField(_('نام کامل'), max_length=200, blank=True)
    phone = models.CharField(_('شماره موبایل'), max_length=15, blank=True, null=True)
    avatar = models.ImageField(_('تصویر پروفایل'), upload_to='avatars/', null=True, blank=True)
    role = models.CharField(_('نقش'), max_length=20, choices=ROLE_CHOICES, default='user')
    gender = models.CharField(_('جنسیت'), max_length=10, choices=GENDER_CHOICES, blank=True)
    bio = models.TextField(_('بیوگرافی'), blank=True)
    birth_date = models.DateField(_('تاریخ تولد'), null=True, blank=True)
    city = models.CharField(_('شهر'), max_length=100, blank=True)
    country = models.CharField(_('کشور'), max_length=100, blank=True)
    website = models.URLField(_('وب‌سایت'), blank=True)
    interest = models.CharField(_('علاقه'), max_length=200, blank=True)

    class Meta:
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربران')

    def save(self, *args, **kwargs):
        if not self.full_name:
            self.full_name = f'{self.first_name} {self.last_name}'.strip() or self.username
        super().save(*args, **kwargs)

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return '/static/assets/images/dashboard/profile.png'

    def __str__(self):
        return self.full_name or self.username
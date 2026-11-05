from django.db import models
from django.conf import settings


class ContactGroup(models.Model):
    name = models.CharField('نام گروه', max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'گروه مخاطبین'
        verbose_name_plural = 'گروه‌های مخاطبین'

    def __str__(self):
        return self.name


class Contact(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contacts')
    first_name = models.CharField('نام', max_length=100)
    last_name = models.CharField('نام خانوادگی', max_length=100, blank=True)
    email = models.EmailField('ایمیل', blank=True)
    phone = models.CharField('تلفن', max_length=20, blank=True)
    phone_type = models.CharField('نوع تلفن', max_length=20, default='mobile')
    group = models.ForeignKey(ContactGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name='contacts')
    avatar = models.ImageField('تصویر', upload_to='contacts/', null=True, blank=True)
    gender = models.CharField('جنسیت', max_length=10, blank=True)
    city = models.CharField('شهر', max_length=100, blank=True)
    bio = models.TextField('درباره', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'مخاطب'
        verbose_name_plural = 'مخاطبین'
        ordering = ['first_name']

    def full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()

    def __str__(self):
        return self.full_name()
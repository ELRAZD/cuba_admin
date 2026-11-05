from django.db import models
from django.conf import settings


class Notification(models.Model):
    TYPES = (
        ('order', 'سفارش'),
        ('message', 'پیام'),
        ('task', 'وظیفه'),
        ('system', 'سیستمی'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField('عنوان', max_length=200)
    body = models.TextField('متن', blank=True)
    type = models.CharField('نوع', max_length=20, choices=TYPES, default='system')
    is_read = models.BooleanField('خوانده شده', default=False)
    link = models.CharField('لینک', max_length=300, blank=True)
    created_at = models.DateTimeField('تاریخ', auto_now_add=True)

    class Meta:
        verbose_name = 'اعلان'
        verbose_name_plural = 'اعلان‌ها'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


def create_notification(user, title, body='', ntype='system', link=''):
    return Notification.objects.create(
        user=user, title=title, body=body, type=ntype, link=link,
    )
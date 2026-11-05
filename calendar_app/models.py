from django.db import models
from django.conf import settings


class Event(models.Model):
    title = models.CharField('عنوان', max_length=200)
    description = models.TextField('توضیحات', blank=True)
    start = models.DateTimeField('شروع')
    end = models.DateTimeField('پایان', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    color = models.CharField('رنگ', max_length=20, default='#7366ff')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'رویداد'
        verbose_name_plural = 'رویدادها'
        ordering = ['start']

    def __str__(self):
        return self.title
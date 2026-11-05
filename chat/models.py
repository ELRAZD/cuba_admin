from django.db import models
from django.conf import settings


class ChatRoom(models.Model):
    ROOM_TYPES = (('private', 'خصوصی'), ('group', 'گروهی'))
    name = models.CharField('نام', max_length=100, blank=True)
    room_type = models.CharField('نوع', max_length=10, choices=ROOM_TYPES, default='private')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'اتاق چت'
        verbose_name_plural = 'اتاق‌های چت'

    def __str__(self):
        return self.name or f'Room #{self.pk}'


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField('متن')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام‌ها'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.sender}: {self.body[:30]}'
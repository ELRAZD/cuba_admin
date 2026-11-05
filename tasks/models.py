from django.db import models
from django.conf import settings


class Project(models.Model):
    name = models.CharField('نام پروژه', max_length=200)
    description = models.TextField('توضیحات', blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='مالک')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='projects', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'پروژه'
        verbose_name_plural = 'پروژه‌ها'

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS = (
        ('todo', 'برای انجام'),
        ('in_progress', 'در حال انجام'),
        ('review', 'بازبینی'),
        ('done', 'انجام شده'),
    )
    PRIORITY = (('low', 'کم'), ('medium', 'متوسط'), ('high', 'زیاد'))

    title = models.CharField('عنوان', max_length=250)
    description = models.TextField('توضیحات', blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='مسئول')
    status = models.CharField('وضعیت', max_length=20, choices=STATUS, default='todo')
    priority = models.CharField('اولویت', max_length=10, choices=PRIORITY, default='medium')
    due_date = models.DateField('مهلت', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'وظیفه'
        verbose_name_plural = 'وظایف'

    def __str__(self):
        return self.title
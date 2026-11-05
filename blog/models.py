from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager


class Category(models.Model):
    name = models.CharField('نام دسته', max_length=100)
    slug = models.SlugField('اسلاگ', unique=True, allow_unicode=True)

    class Meta:
        verbose_name = 'دسته'
        verbose_name_plural = 'دسته‌بندی‌ها'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'پیش‌نویس'),
        ('published', 'منتشر شده'),
    )

    title = models.CharField('عنوان', max_length=300)
    slug = models.SlugField('اسلاگ', unique=True, allow_unicode=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='نویسنده')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='دسته')
    content = RichTextUploadingField('محتوا')
    summary = models.TextField('خلاصه', blank=True)
    image = models.ImageField('تصویر اصلی', upload_to='blog/', null=True, blank=True)
    status = models.CharField('وضعیت', max_length=20, choices=STATUS_CHOICES, default='draft')
    views = models.PositiveIntegerField('بازدید', default=0)
    tags = TaggableManager('برچسب‌ها', blank=True)
    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ به‌روزرسانی', auto_now=True)

    class Meta:
        verbose_name = 'پست'
        verbose_name_plural = 'پست‌ها'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='پست')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='نویسنده')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='replies', verbose_name='پاسخ به')
    body = models.TextField('متن نظر')
    is_approved = models.BooleanField('تأیید شده', default=False)
    created_at = models.DateTimeField('تاریخ', auto_now_add=True)

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'
        ordering = ['created_at']

    def __str__(self):
        return f'نظر از {self.author} روی {self.post}'
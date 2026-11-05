from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from decimal import Decimal


class Category(models.Model):
    name = models.CharField('نام', max_length=150)
    slug = models.SlugField(unique=True, allow_unicode=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    image = models.ImageField(upload_to='categories/', null=True, blank=True)

    class Meta:
        verbose_name = 'دسته'
        verbose_name_plural = 'دسته‌ها'

    def __str__(self):
        return self.name


class Product(models.Model):
    STATUS = (
        ('in_stock', 'موجود در انبار'),
        ('out_of_stock', 'ناموجود'),
        ('preorder', 'پیش‌سفارش'),
    )
    name = models.CharField('نام محصول', max_length=250)
    slug = models.SlugField(unique=True, allow_unicode=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='دسته')
    description = models.TextField('توضیحات')
    short_description = models.TextField('توضیح کوتاه', blank=True)
    price = models.DecimalField('قیمت', max_digits=12, decimal_places=0)
    discount_price = models.DecimalField('قیمت با تخفیف', max_digits=12, decimal_places=0, null=True, blank=True)
    stock = models.PositiveIntegerField('موجودی', default=0)
    status = models.CharField('وضعیت', max_length=20, choices=STATUS, default='in_stock')
    image = models.ImageField('تصویر', upload_to='products/')
    sku = models.CharField('SKU', max_length=50, blank=True)
    is_active = models.BooleanField('فعال', default=True)
    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_price(self):
        return self.discount_price if self.discount_price is not None else self.price

    def get_absolute_url(self):
        return reverse('ecommerce:product_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')
    alt = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = 'تصویر محصول'
        verbose_name_plural = 'تصاویر محصول'


class Order(models.Model):
    STATUS = (
        ('pending', 'در انتظار پرداخت'),
        ('paid', 'پرداخت شده'),
        ('shipped', 'ارسال شده'),
        ('delivered', 'تحویل داده شده'),
        ('cancelled', 'لغو شده'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='کاربر')
    full_name = models.CharField('نام کامل', max_length=200)
    email = models.EmailField('ایمیل')
    phone = models.CharField('تلفن', max_length=15)
    address = models.TextField('آدرس')
    city = models.CharField('شهر', max_length=100)
    postal_code = models.CharField('کد پستی', max_length=20, blank=True)
    total_price = models.DecimalField('مبلغ کل', max_digits=12, decimal_places=0, default=0)
    status = models.CharField('وضعیت', max_length=20, choices=STATUS, default='pending')
    payment_method = models.CharField('روش پرداخت', max_length=50, default='online')
    created_at = models.DateTimeField('تاریخ سفارش', auto_now_add=True)

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'
        ordering = ['-created_at']

    def __str__(self):
        return f'سفارش #{self.pk} - {self.full_name}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='سفارش')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='محصول')
    price = models.DecimalField('قیمت واحد', max_digits=12, decimal_places=0)
    quantity = models.PositiveIntegerField('تعداد', default=1)

    class Meta:
        verbose_name = 'آیتم سفارش'
        verbose_name_plural = 'آیتم‌های سفارش'

    def get_total(self):
        return self.price * self.quantity


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total(self):
        return sum(item.get_total() for item in self.items.all())

    def __str__(self):
        return f'سبد {self.user}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total(self):
        return self.product.get_price() * self.quantity

    def __str__(self):
        return f'{self.product} x {self.quantity}'


class Invoice(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='invoice', verbose_name='سفارش')
    invoice_number = models.CharField('شماره فاکتور', max_length=50, unique=True)
    issued_at = models.DateTimeField('تاریخ صدور', auto_now_add=True)
    notes = models.TextField('یادداشت', blank=True)

    class Meta:
        verbose_name = 'فاکتور'
        verbose_name_plural = 'فاکتورها'

    def __str__(self):
        return self.invoice_number

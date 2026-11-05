from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from django.db import transaction
from decimal import Decimal

from .models import Product, Category, Order, OrderItem, Invoice
from .cart import get_or_create_cart, add_to_cart, remove_from_cart, clear_cart
from .forms import OrderForm
from django.views.decorators.http import require_POST


def product_list(request):
    products = Product.objects.filter(is_active=True)
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    return render(request, 'ecommerce/products.html', {
        'products': paginator.get_page(page),
        'categories': Category.objects.all(),
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related = Product.objects.filter(category=product.category, is_active=True).exclude(pk=product.pk)[:4]
    return render(request, 'ecommerce/product_page.html', {
        'product': product, 'related': related,
    })


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'ecommerce/category.html', {'categories': categories})


@login_required
def cart_view(request):
    cart = get_or_create_cart(request.user)
    return render(request, 'ecommerce/cart.html', {
        'cart': cart, 'items': cart.items.all(), 'total': cart.get_total(),
    })


@login_required
@require_POST
def cart_add(request, product_id):
    try:
        qty = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        messages.error(request, 'تعداد محصول نامعتبر است.')
        return redirect('ecommerce:products')

    if qty < 1:
        messages.error(request, 'تعداد محصول باید حداقل یک باشد.')
        return redirect('ecommerce:products')

    product = get_object_or_404(
        Product,
        pk=product_id,
        is_active=True,
        status='in_stock'
    )

    if qty > product.stock:
        messages.error(request, 'موجودی محصول کافی نیست.')
        return redirect('ecommerce:cart')

    add_to_cart(request.user, product_id, qty)

    messages.success(request, 'محصول به سبد خرید اضافه شد.')

    return redirect('ecommerce:cart')


@login_required
@require_POST
def cart_remove(request, item_id):
    remove_from_cart(request.user, item_id)

    messages.info(request, 'محصول از سبد خرید حذف شد.')

    return redirect('ecommerce:cart')

@login_required
def checkout(request):
    cart = get_or_create_cart(request.user)
    if not cart.items.exists():
        messages.warning(request, 'سبد خرید شما خالی است.')
        return redirect('ecommerce:cart')

    form = OrderForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = cart.get_total()
            order.save()
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order, product=item.product,
                    price=item.product.get_price(), quantity=item.quantity,
                )
            Invoice.objects.create(
                order=order,
                invoice_number=f'INV-{order.pk:06d}',
            )
            clear_cart(request.user)
        messages.success(request, f'سفارش #{order.pk} با موفقیت ثبت شد.')
        return redirect('ecommerce:order_success', pk=order.pk)
    return render(request, 'ecommerce/checkout.html', {
        'cart': cart, 'form': form, 'total': cart.get_total(),
    })


@login_required
def order_success(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'ecommerce/order_success.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'ecommerce/order_history.html', {'orders': orders})


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'ecommerce/payment_details.html', {'order': order})


@login_required
def invoice_list(request):
    invoices = Invoice.objects.filter(order__user=request.user)
    return render(request, 'ecommerce/invoice_list.html', {'invoices': invoices})


@login_required
def invoice_detail(request, invoice_number):
    invoice = get_object_or_404(Invoice, invoice_number=invoice_number, order__user=request.user)
    return render(request, 'ecommerce/invoice.html', {'invoice': invoice})


def pricing(request):
    return render(request, 'ecommerce/pricing.html')
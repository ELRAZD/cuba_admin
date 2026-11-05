from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

from ecommerce.models import Order, Product
from accounts.models import User
from blog.models import Post
from tasks.models import Task


@login_required
def index(request):
    now = timezone.now()
    last_month = now - timedelta(days=30)

    context = {
        'total_orders': Order.objects.count(),
        'total_users': User.objects.count(),
        'total_products': Product.objects.count(),
        'total_posts': Post.objects.count(),
        'pending_tasks': Task.objects.filter(status='todo').count(),
        'recent_orders': Order.objects.order_by('-created_at')[:5],
        'recent_users': User.objects.order_by('-date_joined')[:5],
        'monthly_sales': Order.objects.filter(created_at__gte=last_month)
                                      .aggregate(total=Sum('total_price'))['total'] or 0,
    }
    return render(request, 'dashboard/dashboard_01.html', context)


@login_required
def ecommerce_dashboard(request):
    now = timezone.now()
    last_30 = now - timedelta(days=30)

    context = {
        'orders_count': Order.objects.count(),
        'new_orders': Order.objects.filter(created_at__gte=last_30).count(),
        'revenue': Order.objects.aggregate(total=Sum('total_price'))['total'] or 0,
        'customers_count': User.objects.filter(role='user').count(),
        'top_products': Product.objects.annotate(
            sold=Count('orderitem')
        ).order_by('-sold')[:5],
        'recent_orders': Order.objects.order_by('-created_at')[:10],
    }
    return render(request, 'dashboard/dashboard_02.html', context)


@login_required
def online_course_dashboard(request):
    return render(request, 'dashboard/dashboard_03.html')


@login_required
def crypto_dashboard(request):
    return render(request, 'dashboard/dashboard_04.html')


@login_required
def social_dashboard(request):
    return render(request, 'dashboard/dashboard_05.html')


@login_required
def nft_dashboard(request):
    return render(request, 'dashboard/dashboard_06.html')


@login_required
def school_dashboard(request):
    return render(request, 'dashboard/dashboard_07.html')


@login_required
def pos_dashboard(request):
    return render(request, 'dashboard/dashboard_08.html')
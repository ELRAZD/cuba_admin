from django.urls import path
from . import views

app_name = 'ecommerce'

urlpatterns = [
    path('products/', views.product_list, name='products'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('categories/', views.category_list, name='categories'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:item_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/success/<int:pk>/', views.order_success, name='order_success'),
    path('orders/', views.order_history, name='order_history'),
    path('order/<int:pk>/', views.order_detail, name='order_detail'),
    path('invoices/', views.invoice_list, name='invoices'),
    path('invoice/<str:invoice_number>/', views.invoice_detail, name='invoice_detail'),
    path('pricing/', views.pricing, name='pricing'),
]
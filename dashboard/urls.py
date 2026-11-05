from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.index, name='dashboard'),
    path('dashboard/ecommerce/', views.ecommerce_dashboard, name='ecommerce'),
    path('dashboard/course/', views.online_course_dashboard, name='course'),
    path('dashboard/crypto/', views.crypto_dashboard, name='crypto'),
    path('dashboard/social/', views.social_dashboard, name='social'),
    path('dashboard/nft/', views.nft_dashboard, name='nft'),
    path('dashboard/school/', views.school_dashboard, name='school'),
    path('dashboard/pos/', views.pos_dashboard, name='pos'),
]
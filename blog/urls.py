from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='list'),
    path('post/<slug:slug>/', views.post_detail, name='detail'),
    path('add-post/', views.add_post, name='add_post'),
]
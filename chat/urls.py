from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_home, name='home'),
    path('private/<int:user_id>/', views.private_chat, name='private_chat'),
    path('group/', views.group_chat, name='group_chat'),
    path('video/', views.chat_video, name='video'),
]
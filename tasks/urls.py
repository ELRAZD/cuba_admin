from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.task_list, name='list'),
    path('kanban/', views.kanban_board, name='kanban'),
    path('create/', views.task_create, name='create'),
    path('<int:pk>/status/', views.task_update_status, name='update_status'),
]
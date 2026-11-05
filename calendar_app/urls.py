from django.urls import path
from . import views

app_name = 'calendar_app'

urlpatterns = [
    path('', views.calendar_view, name='calendar'),
    path('events.json', views.events_json, name='events_json'),
    path('add/', views.add_event, name='add'),
]
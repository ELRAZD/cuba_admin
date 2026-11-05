from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('accounts/', include('accounts.urls')),
    path('', include('dashboard.urls')),
    path('blog/', include('blog.urls')),
    path('shop/', include('ecommerce.urls')),
    path('chat/', include('chat.urls')),
    path('contacts/', include('contacts.urls')),
    path('tasks/', include('tasks.urls')),
    path('calendar/', include('calendar_app.urls')),
    path('notifications/', include('notifications.urls')),
    path('blog/', include('blog.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

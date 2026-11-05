from notifications.models import Notification

def site_context(request):
    site_name = 'پنل مدیریت کوبا'
    return {
        'site_name': site_name,
        'user': request.user if request.user.is_authenticated else None,
    }

def notifications_context(request):
    if request.user.is_authenticated:
        unread = Notification.objects.filter(user=request.user, is_read=False)[:5]
        return {
            'unread_notifications': unread,
            'unread_count': Notification.objects.filter(user=request.user, is_read=False).count(),
        }
    return {'unread_notifications': [], 'unread_count': 0}
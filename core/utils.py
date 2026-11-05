from django.utils import timezone
from datetime import timedelta

def time_ago(dt):
    """تبدیل تاریخ به 'چند لحظه پیش'"""
    now = timezone.now()
    diff = now - dt
    seconds = diff.total_seconds()
    if seconds < 60:
        return 'همین الان'
    elif seconds < 3600:
        return f'{int(seconds // 60)} دقیقه پیش'
    elif seconds < 86400:
        return f'{int(seconds // 3600)} ساعت پیش'
    elif seconds < 604800:
        return f'{int(seconds // 86400)} روز پیش'
    else:
        return dt.strftime('%Y/%m/%d')
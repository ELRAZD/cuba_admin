from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification
from django.views.decorators.http import require_POST


@login_required
def notification_list(request):
    notifications = request.user.notifications.all()
    return render(request, 'notifications/list.html', {'notifications': notifications})


@login_required
@require_POST
def mark_all_read(request):
    request.user.notifications.filter(
        is_read=False
    ).update(is_read=True)

    return redirect('notifications:list')
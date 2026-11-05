from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Event


@login_required
def calendar_view(request):
    return render(request, 'calendar_app/calendar.html')


@login_required
def events_json(request):
    events = Event.objects.filter(user=request.user)
    data = [{
        'id': e.id, 'title': e.title, 'start': e.start.isoformat(),
        'end': e.end.isoformat() if e.end else None,
        'backgroundColor': e.color,
    } for e in events]
    return JsonResponse(data, safe=False)


@login_required
def add_event(request):
    if request.method == 'POST':
        Event.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description', ''),
            start=request.POST.get('start'),
            end=request.POST.get('end') or None,
            user=request.user,
        )
    return redirect('calendar_app:calendar')
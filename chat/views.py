from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db.models import Count

from .models import ChatRoom, Message
from django.http import JsonResponse
from django.utils import timezone

User = get_user_model()


def _get_or_create_private_room(user1, user2):
    room = (
        ChatRoom.objects.filter(
            room_type='private',
            participants=user1,
        )
        .filter(participants=user2)
        .annotate(
            num_participants=Count('participants', distinct=True)
        )
        .filter(num_participants=2)
        .first()
    )

    if room is None:
        room = ChatRoom.objects.create(room_type='private')
        room.participants.add(user1, user2)

    return room


@login_required
def chat_home(request):
    all_users = User.objects.exclude(pk=request.user.pk).filter(is_active=True)[:20]
    rooms = request.user.chat_rooms.all()

    active_user = all_users[0] if all_users.exists() else None
    messages_list = []
    active_room = None

    if active_user:
        active_room = _get_or_create_private_room(request.user, active_user)
        messages_list = active_room.messages.select_related('sender').order_by('created_at')
        messages_list.exclude(sender=request.user).update(is_read=True)

    return render(request, 'chat/chat.html', {
        'all_users': all_users,
        'rooms': rooms,
        'active_user': active_user,
        'active_room': active_room,
        'messages': messages_list,
    })


@login_required
def private_chat(request, user_id):
    other = get_object_or_404(User, pk=user_id)
    room = _get_or_create_private_room(request.user, other)

    if request.method == 'POST':
        body = request.POST.get('body', '').strip()
        if body:
            Message.objects.create(room=room, sender=request.user, body=body)
        return redirect('chat:private_chat', user_id=user_id)

    msgs = room.messages.select_related('sender').order_by('created_at')
    msgs.exclude(sender=request.user).update(is_read=True)

    all_users = User.objects.exclude(pk=request.user.pk).filter(is_active=True)[:20]
    rooms = request.user.chat_rooms.all()

    return render(request, 'chat/chat.html', {
        'all_users': all_users,
        'rooms': rooms,
        'active_user': other,
        'active_room': room,
        'messages': msgs,
    })


@login_required
def group_chat(request):
    rooms = request.user.chat_rooms.filter(room_type='group')

    active_room = rooms.first() if rooms.exists() else None
    messages_list = []
    if active_room:
        messages_list = active_room.messages.select_related('sender').order_by('created_at')

    if request.method == 'POST' and active_room:
        body = request.POST.get('body', '').strip()
        if body:
            Message.objects.create(room=active_room, sender=request.user, body=body)
        return redirect('chat:group_chat')

    return render(request, 'chat/group_chat.html', {
        'rooms': rooms,
        'active_room': active_room,
        'messages': messages_list,
    })


@login_required
def chat_video(request):
    all_users = User.objects.exclude(pk=request.user.pk).filter(is_active=True)[:20]
    return render(request, 'chat/chat_video.html', {
        'all_users': all_users,
    })

@login_required
def chat_messages_api(request, room_id):
    room = get_object_or_404(
        ChatRoom,
        pk=room_id,
        room_type='private',
        participants=request.user
    )

    try:
        after_id = int(request.GET.get('after', 0))
    except (ValueError, TypeError):
        after_id = 0

    new_messages = (
        room.messages
        .filter(pk__gt=after_id)
        .select_related('sender')
        .order_by('created_at')
    )

    data = []

    for msg in new_messages:
        data.append({
            'id': msg.id,
            'sender_id': msg.sender_id,
            'body': msg.body,
            'created_at': timezone.localtime(
                msg.created_at
            ).strftime('%H:%M'),
        })

    room.messages.filter(
        pk__in=[msg['id'] for msg in data]
    ).exclude(sender=request.user).update(is_read=True)

    return JsonResponse({
        'messages': data
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Task, Project
from .forms import TaskForm


def get_user_tasks(user):
    return Task.objects.filter(
        Q(assignee=user) |
        Q(project__owner=user) |
        Q(project__members=user)
    ).distinct()


@login_required
def task_list(request):
    return redirect('tasks:kanban')


@login_required
def kanban_board(request):
    tasks = get_user_tasks(request.user)

    columns = {
        'todo': tasks.filter(status='todo'),
        'in_progress': tasks.filter(status='in_progress'),
        'review': tasks.filter(status='review'),
        'done': tasks.filter(status='done'),
    }

    return render(request, 'tasks/kanban.html', {
        'columns': columns
    })


@login_required
def task_create(request):
    form = TaskForm(
        request.POST or None,
        user=request.user
    )

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('tasks:kanban')

    return render(request, 'tasks/task_form.html', {
        'form': form
    })


@login_required
def task_update_status(request, pk):
    if request.method != 'POST':
        return redirect('tasks:kanban')

    task = get_object_or_404(
        get_user_tasks(request.user),
        pk=pk
    )

    new_status = request.POST.get('status')

    if new_status in dict(Task.STATUS):
        task.status = new_status
        task.save(update_fields=['status'])

    return redirect('tasks:kanban')
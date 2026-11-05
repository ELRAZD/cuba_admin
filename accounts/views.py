from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect

from .forms import LoginForm, RegisterForm, ProfileForm
from django.views.decorators.http import require_POST


@csrf_protect
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, 'با موفقیت وارد شدید.')
        return redirect('dashboard:index')
    return render(request, 'accounts/login.html', {'form': form})


@login_required
@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, 'با موفقیت خارج شدید.')
    return redirect('accounts:login')


@csrf_protect
def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'ثبت‌نام با موفقیت انجام شد.')
        return redirect('dashboard:index')
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile_view(request):
    user = request.user
    return render(request, 'accounts/profile.html', {'profile_user': user})


@login_required
def edit_profile_view(request):
    form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'پروفایل با موفقیت به‌روزرسانی شد.')
        return redirect('accounts:profile')
    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def user_cards_view(request):
    from .models import User
    users = User.objects.filter(is_active=True)
    return render(request, 'accounts/user_cards.html', {'users': users})
"""
Authentication views for login, logout, password reset, and verification.
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from django.http import JsonResponse
from ..services.auth_service import AuthService
from ..services.user_service import UserService
from ..forms.auth_forms import LoginForm, ForgotPasswordForm, ResetPasswordForm, ChangePasswordForm
import logging

logger = logging.getLogger(__name__)


def splash(request):
    """Splash screen view."""
    if request.user.is_authenticated:
        return redirect('authentication:dashboard')
    return render(request, 'splash.html')


def login_view(request):
    """Login view."""
    if request.user.is_authenticated:
        return redirect('authentication:dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me', False)

            success, user, error = AuthService.authenticate_user(
                username, password, request, remember_me
            )

            if success:
                messages.success(request, f'Welcome back, {user.get_full_name()}!')
                return redirect('authentication:dashboard')
            else:
                messages.error(request, error or 'Invalid credentials')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    """Logout view."""
    AuthService.logout_user(request)
    messages.info(request, 'You have been logged out.')
    return redirect('authentication:login')


@login_required
def dashboard(request):
    """Dashboard view."""
    context = {
        'user': request.user,
        'last_login': request.user.last_login,
        'company_name': 'FabricERP',
        'app_version': '1.0.0',
    }
    return render(request, 'dashboard.html', context)


def forgot_password(request):
    """Forgot password view."""
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            success, message = AuthService.forgot_password(email, request)
            messages.success(request, message)
            return redirect('authentication:login')
    else:
        form = ForgotPasswordForm()

    return render(request, 'forgot_password.html', {'form': form})


def reset_password(request, uidb64, token):
    """Reset password view."""
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            success, message = AuthService.reset_password(uidb64, token, new_password)
            if success:
                messages.success(request, message)
                return redirect('authentication:login')
            else:
                messages.error(request, message)
    else:
        form = ResetPasswordForm()

    return render(request, 'reset_password.html', {
        'form': form,
        'uidb64': uidb64,
        'token': token
    })


@login_required
def change_password(request):
    """Change password view."""
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['new_password']
            success, message = AuthService.change_password(
                request.user, current_password, new_password
            )
            if success:
                messages.success(request, message)
                return redirect('authentication:dashboard')
            else:
                messages.error(request, message)
    else:
        form = ChangePasswordForm()

    return render(request, 'change_password.html', {'form': form})


def verify_email(request, uidb64, token):
    """Verify email view."""
    success, message = AuthService.verify_email(uidb64, token)
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)
    return redirect('authentication:login')


def resend_verification(request):
    """Resend verification email view."""
    if request.method == 'POST':
        email = request.POST.get('email')
        success, message = AuthService.resend_verification(email, request)
        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)
        return redirect('authentication:login')

    return render(request, 'resend_verification.html')


def account_locked(request):
    """Account locked view."""
    return render(request, 'account_locked.html')
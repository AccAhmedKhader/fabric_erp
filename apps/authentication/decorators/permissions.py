"""
Permission checking decorators.
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


def permission_required(permission_code):
    """
    Decorator that checks if a user has a specific permission.

    Args:
        permission_code: The permission code to check

    Returns:
        Decorated view function
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(reverse('authentication:login'))

            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            from ..repositories.user_repository import UserRepository

            if UserRepository.has_permission(request.user, permission_code):
                return view_func(request, *args, **kwargs)

            messages.error(request, 'You do not have permission to access this page.')
            return redirect(reverse('authentication:dashboard'))

        return _wrapped_view
    return decorator
"""
User management views for CRUD operations.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from ..services.user_service import UserService
from ..repositories.user_repository import UserRepository
from ..forms.user_forms import UserForm, UserEditForm
from ..decorators.permissions import permission_required
import logging

logger = logging.getLogger(__name__)


@login_required
@permission_required('manage_users')
def user_list(request):
    """List all users."""
    search = request.GET.get('search', '')
    is_active = request.GET.get('is_active')

    if is_active in ('True', 'False'):
        is_active = is_active == 'True'
    else:
        is_active = None

    users = UserRepository.get_all(search=search, is_active=is_active)

    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'users/list.html', {
        'page_obj': page_obj,
        'search': search,
        'is_active': is_active,
    })


@login_required
@permission_required('manage_users')
def user_add(request):
    """Add a new user."""
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            success, user, errors = UserService.create_user(form.cleaned_data)
            if success:
                messages.success(request, f'User {user.username} created successfully!')
                return redirect('authentication:user_list')
            else:
                for error in errors:
                    messages.error(request, error)
    else:
        form = UserForm()

    return render(request, 'users/add.html', {'form': form})


@login_required
@permission_required('manage_users')
def user_edit(request, user_id):
    """Edit an existing user."""
    user = get_object_or_404(UserRepository.get_by_id(user_id))

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            success, updated_user, errors = UserService.update_user(
                user_id, form.cleaned_data
            )
            if success:
                messages.success(request, f'User {updated_user.username} updated successfully!')
                return redirect('authentication:user_list')
            else:
                for error in errors:
                    messages.error(request, error)
    else:
        form = UserEditForm(instance=user)

    return render(request, 'users/edit.html', {'form': form, 'user': user})


@login_required
@permission_required('manage_users')
def user_delete(request, user_id):
    """Delete a user."""
    user = get_object_or_404(UserRepository.get_by_id(user_id))

    if request.method == 'POST':
        success, message = UserService.delete_user(user_id)
        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)
        return redirect('authentication:user_list')

    return render(request, 'users/delete.html', {'user': user})


@login_required
@permission_required('manage_users')
def user_toggle_active(request, user_id):
    """Toggle user active status."""
    if request.method == 'POST':
        success, user, message = UserService.toggle_user_active(user_id)
        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)
    return redirect('authentication:user_list')
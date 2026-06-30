"""
Permission management views for CRUD operations.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from ..services.permission_service import PermissionService
from ..repositories.permission_repository import PermissionRepository
from ..forms.permission_forms import PermissionForm
from ..decorators.permissions import permission_required
import logging

logger = logging.getLogger(__name__)


@login_required
@permission_required('manage_permissions')
def permission_list(request):
    """List all permissions."""
    search = request.GET.get('search', '')
    category = request.GET.get('category', '')

    permissions = PermissionRepository.get_all(search=search, category=category)

    paginator = Paginator(permissions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = PermissionRepository.get_categories()

    return render(request, 'permissions/list.html', {
        'page_obj': page_obj,
        'search': search,
        'category': category,
        'categories': categories,
    })


@login_required
@permission_required('manage_permissions')
def permission_add(request):
    """Add a new permission."""
    if request.method == 'POST':
        form = PermissionForm(request.POST)
        if form.is_valid():
            success, permission, errors = PermissionService.create_permission(
                form.cleaned_data
            )
            if success:
                messages.success(request, f'Permission {permission.name} created successfully!')
                return redirect('authentication:permission_list')
            else:
                for error in errors:
                    messages.error(request, error)
    else:
        form = PermissionForm()

    return render(request, 'permissions/add.html', {'form': form})


@login_required
@permission_required('manage_permissions')
def permission_delete(request, permission_id):
    """Delete a permission."""
    permission = get_object_or_404(PermissionRepository.get_by_id(permission_id))

    if request.method == 'POST':
        success, message = PermissionService.delete_permission(permission_id)
        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)
        return redirect('authentication:permission_list')

    return render(request, 'permissions/delete.html', {'permission': permission})
"""
Role management views for CRUD operations.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from ..services.role_service import RoleService
from ..repositories.role_repository import RoleRepository
from ..repositories.permission_repository import PermissionRepository
from ..forms.role_forms import RoleForm, RoleEditForm
from ..decorators.permissions import permission_required
import logging

logger = logging.getLogger(__name__)


@login_required
@permission_required('manage_roles')
def role_list(request):
    """List all roles."""
    search = request.GET.get('search', '')
    roles = RoleRepository.get_all(search=search)

    paginator = Paginator(roles, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'roles/list.html', {
        'page_obj': page_obj,
        'search': search,
    })


@login_required
@permission_required('manage_roles')
def role_add(request):
    """Add a new role."""
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            success, role, errors = RoleService.create_role(form.cleaned_data)
            if success:
                messages.success(request, f'Role {role.name} created successfully!')
                return redirect('authentication:role_list')
            else:
                for error in errors:
                    messages.error(request, error)
    else:
        form = RoleForm()

    return render(request, 'roles/add.html', {'form': form})


@login_required
@permission_required('manage_roles')
def role_edit(request, role_id):
    """Edit an existing role."""
    role = get_object_or_404(RoleRepository.get_by_id(role_id))

    if request.method == 'POST':
        form = RoleEditForm(request.POST, instance=role)
        if form.is_valid():
            success, updated_role, errors = RoleService.update_role(
                role_id, form.cleaned_data
            )
            if success:
                messages.success(request, f'Role {updated_role.name} updated successfully!')
                return redirect('authentication:role_list')
            else:
                for error in errors:
                    messages.error(request, error)
    else:
        form = RoleEditForm(instance=role)

    return render(request, 'roles/edit.html', {'form': form, 'role': role})


@login_required
@permission_required('manage_roles')
def role_delete(request, role_id):
    """Delete a role."""
    role = get_object_or_404(RoleRepository.get_by_id(role_id))

    if request.method == 'POST':
        success, message = RoleService.delete_role(role_id)
        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)
        return redirect('authentication:role_list')

    return render(request, 'roles/delete.html', {'role': role})


@login_required
@permission_required('manage_roles')
def role_assign_permissions(request, role_id):
    """Assign permissions to a role."""
    role = get_object_or_404(RoleRepository.get_by_id(role_id))

    if request.method == 'POST':
        permission_ids = request.POST.getlist('permissions')
        permission_ids = [pid for pid in permission_ids if pid]

        success, message = RoleService.assign_permissions(role_id, permission_ids)
        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)
        return redirect('authentication:role_list')

    permissions = PermissionRepository.get_all()
    assigned_permissions = role.enterprise_permissions.all().values_list('id', flat=True)

    return render(request, 'roles/assign_permissions.html', {
        'role': role,
        'permissions': permissions,
        'assigned_permissions': assigned_permissions,
    })
"""
Repository pattern implementation for Permission model.
"""

from typing import Optional, List, Dict, Any
from uuid import UUID
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, QuerySet
from ..models import EnterprisePermission, PermissionCategory


class PermissionRepository:
    """
    Repository for Permission model operations.
    """

    @staticmethod
    def get_by_id(permission_id: UUID) -> Optional[EnterprisePermission]:
        """Get a permission by UUID."""
        try:
            return EnterprisePermission.objects.get(id=permission_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_by_code(code: str) -> Optional[EnterprisePermission]:
        """Get a permission by code."""
        try:
            return EnterprisePermission.objects.get(django_permission__codename=code)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_all(
        search: Optional[str] = None,
        category: Optional[str] = None,
        order_by: str = 'django_permission__codename'
    ) -> QuerySet:
        """Get all permissions with optional filters."""
        queryset = EnterprisePermission.objects.all()

        if search:
            queryset = queryset.filter(
                Q(django_permission__name__icontains=search) |
                Q(django_permission__codename__icontains=search) |
                Q(description__icontains=search)
            )

        if category:
            queryset = queryset.filter(category__code=category)

        return queryset.order_by(order_by)

    @staticmethod
    def get_by_category(category_code: str) -> QuerySet:
        """Get all permissions for a specific category."""
        return EnterprisePermission.objects.filter(
            category__code=category_code
        ).order_by('django_permission__codename')

    @staticmethod
    @transaction.atomic
    def create(permission_data: Dict[str, Any]) -> EnterprisePermission:
        """Create a new permission."""
        return EnterprisePermission.create_enterprise_permission(**permission_data)

    @staticmethod
    @transaction.atomic
    def delete(permission_id: UUID) -> bool:
        """Delete a permission."""
        permission = PermissionRepository.get_by_id(permission_id)
        if not permission or permission.is_system:
            return False
        permission.delete()
        return True

    @staticmethod
    def get_categories() -> QuerySet:
        """Get all permission categories."""
        return PermissionCategory.objects.all().order_by('order', 'name')

    @staticmethod
    def get_modules() -> List[str]:
        """Get all unique module names."""
        return PermissionCategory.objects.values_list('code', flat=True).distinct().order_by('code')
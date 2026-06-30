"""
Service layer for permission management operations.
"""

import logging
from typing import Optional, List, Dict, Any, Tuple
from uuid import UUID
from django.db import transaction
from ..repositories.permission_repository import PermissionRepository

logger = logging.getLogger(__name__)


class PermissionService:
    """
    Service class for handling permission management operations.
    """

    @staticmethod
    def create_permission(permission_data: Dict[str, Any]) -> Tuple[bool, Optional[Any], List[str]]:
        """
        Create a new permission.

        Returns:
            Tuple of (success, permission, errors)
        """
        errors = []

        try:
            if PermissionRepository.get_by_code(permission_data.get('code', '')):
                errors.append('Permission code is already taken')

            if errors:
                return False, None, errors

            permission = PermissionRepository.create(permission_data)
            logger.info(f"Permission created: {permission.codename}")
            return True, permission, []

        except Exception as e:
            logger.error(f"Error creating permission: {str(e)}")
            return False, None, [str(e)]

    @staticmethod
    def delete_permission(permission_id: UUID) -> Tuple[bool, str]:
        """
        Delete a permission.

        Returns:
            Tuple of (success, message)
        """
        try:
            permission = PermissionRepository.get_by_id(permission_id)
            if not permission:
                return False, 'Permission not found'

            PermissionRepository.delete(permission_id)
            logger.info(f"Permission deleted: {permission.codename}")
            return True, 'Permission deleted successfully'

        except Exception as e:
            logger.error(f"Error deleting permission: {str(e)}")
            return False, str(e)

    @staticmethod
    def get_permissions_by_category(category_code: str) -> List[Dict[str, Any]]:
        """
        Get all permissions for a category.

        Returns:
            List of permission dictionaries
        """
        try:
            permissions = PermissionRepository.get_by_category(category_code)
            return [
                {
                    'id': perm.id,
                    'name': perm.name,
                    'code': perm.codename,
                    'description': perm.description,
                }
                for perm in permissions
            ]
        except Exception as e:
            logger.error(f"Error getting category permissions: {str(e)}")
            return []
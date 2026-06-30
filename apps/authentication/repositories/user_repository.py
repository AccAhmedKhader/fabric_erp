"""
Repository pattern implementation for User model.
"""

from typing import Optional, List, Dict, Any
from uuid import UUID
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.db.models import Q, QuerySet

User = get_user_model()


class UserRepository:
    """
    Repository for User model operations.
    """

    @staticmethod
    def get_by_id(user_id: UUID) -> Optional[User]:
        """Get a user by UUID."""
        try:
            return User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_by_username(username: str) -> Optional[User]:
        """Get a user by username."""
        try:
            return User.objects.get(username__iexact=username)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        """Get a user by email."""
        try:
            return User.objects.get(email__iexact=email)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_all(
        search: Optional[str] = None,
        is_active: Optional[bool] = None,
        is_staff: Optional[bool] = None,
        is_superuser: Optional[bool] = None,
        order_by: str = '-created_at'
    ) -> QuerySet:
        """Get all users with optional filters."""
        queryset = User.objects.all()

        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(full_name__icontains=search) |
                Q(email__icontains=search) |
                Q(phone__icontains=search)
            )

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)

        if is_staff is not None:
            queryset = queryset.filter(is_staff=is_staff)

        if is_superuser is not None:
            queryset = queryset.filter(is_superuser=is_superuser)

        return queryset.order_by(order_by)

    @staticmethod
    @transaction.atomic
    def create(user_data: Dict[str, Any]) -> User:
        """Create a new user."""
        password = user_data.pop('password', None)
        user = User(**user_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    @staticmethod
    @transaction.atomic
    def update(user_id: UUID, user_data: Dict[str, Any]) -> Optional[User]:
        """Update an existing user."""
        user = UserRepository.get_by_id(user_id)
        if not user:
            return None

        password = user_data.pop('password', None)
        for key, value in user_data.items():
            setattr(user, key, value)

        if password:
            user.set_password(password)

        user.save()
        return user

    @staticmethod
    @transaction.atomic
    def delete(user_id: UUID) -> bool:
        """Delete a user."""
        user = UserRepository.get_by_id(user_id)
        if not user:
            return False
        user.delete()
        return True

    @staticmethod
    @transaction.atomic
    def toggle_active(user_id: UUID) -> Optional[User]:
        """Toggle user's active status."""
        user = UserRepository.get_by_id(user_id)
        if not user:
            return None
        user.is_active = not user.is_active
        user.save()
        return user

    @staticmethod
    def authenticate(username: str, password: str) -> Optional[User]:
        """Authenticate a user by username and password."""
        try:
            user = User.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
            if user.check_password(password):
                return user
        except ObjectDoesNotExist:
            pass
        return None

    @staticmethod
    def update_last_login(user: User) -> None:
        """Update the user's last login time."""
        user.last_login = user.last_login or user.date_joined
        user.save(update_fields=['last_login'])

    @staticmethod
    def get_users_by_role(role_id: UUID) -> QuerySet:
        """Get all users with a specific role."""
        from apps.authentication.models import Role
        try:
            role = Role.objects.get(id=role_id)
            return role.user_set.all()
        except ObjectDoesNotExist:
            return User.objects.none()

    @staticmethod
    def has_permission(user: User, permission_code: str) -> bool:
        """Check if a user has a specific permission."""
        if user.is_superuser:
            return True

        # Check user permissions directly
        if user.user_permissions.filter(codename=permission_code).exists():
            return True

        # Check through roles
        return user.groups.filter(
            permissions__codename=permission_code
        ).exists()
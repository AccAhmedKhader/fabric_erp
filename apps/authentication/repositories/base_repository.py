"""
Base repository class providing common CRUD operations.
"""

from typing import Optional, List, Dict, Any
from uuid import UUID
from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class BaseRepository:
    """
    Base repository with common CRUD operations.
    """
    model = None

    @classmethod
    def get_by_id(cls, id: UUID) -> Optional[models.Model]:
        """
        Get a model instance by UUID.
        """
        try:
            return cls.model.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    @classmethod
    def get_all(cls, **filters) -> List[models.Model]:
        """
        Get all model instances with optional filters.
        """
        return cls.model.objects.filter(**filters)

    @classmethod
    def create(cls, data: Dict[str, Any]) -> models.Model:
        """
        Create a new model instance.
        """
        return cls.model.objects.create(**data)

    @classmethod
    def update(cls, id: UUID, data: Dict[str, Any]) -> Optional[models.Model]:
        """
        Update a model instance by UUID.
        """
        instance = cls.get_by_id(id)
        if instance:
            for key, value in data.items():
                setattr(instance, key, value)
            instance.save()
            return instance
        return None

    @classmethod
    def delete(cls, id: UUID) -> bool:
        """
        Delete a model instance by UUID.
        """
        instance = cls.get_by_id(id)
        if instance:
            instance.delete()
            return True
        return False
"""
Decorators package for authentication app.
"""

from .permissions import permission_required

__all__ = [
    'permission_required',
]
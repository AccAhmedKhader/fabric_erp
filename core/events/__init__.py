"""
Core event system for the entire application.
Provides a centralized event dispatcher that all modules can use.
"""

from .dispatcher import EventDispatcher, DomainEvent
from .handlers import EventHandler

__all__ = [
    'EventDispatcher',
    'DomainEvent',
    'EventHandler',
]
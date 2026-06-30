"""
Event store for persisting domain events.
"""

import logging
from typing import List, Optional
from datetime import datetime
from .dispatcher import DomainEvent

logger = logging.getLogger(__name__)


class EventStore:
    """
    In-memory event store for testing and development.
    For production, use a persistent event store.
    """

    def __init__(self):
        self._events = []

    def store(self, event: DomainEvent) -> None:
        """
        Store a domain event.
        """
        self._events.append(event)
        logger.debug(f"Stored event: {event.event_type}")

    def get_events(self, aggregate_id: Optional[str] = None) -> List[DomainEvent]:
        """
        Get all events, optionally filtered by aggregate ID.
        """
        if aggregate_id:
            return [e for e in self._events if str(e.aggregate_id) == aggregate_id]
        return self._events.copy()

    def clear(self) -> None:
        """
        Clear all stored events.
        """
        self._events.clear()
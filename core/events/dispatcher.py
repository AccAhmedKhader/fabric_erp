"""
Event dispatcher implementation for domain events.
"""

import logging
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
import threading
import json

logger = logging.getLogger(__name__)


@dataclass
class DomainEvent:
    """Base class for all domain events."""
    event_id: UUID
    event_type: str
    occurred_at: datetime
    aggregate_id: UUID
    aggregate_type: str
    data: dict
    metadata: dict = field(default_factory=dict)

    def to_dict(self):
        """Convert event to dictionary."""
        return {
            'event_id': str(self.event_id),
            'event_type': self.event_type,
            'occurred_at': self.occurred_at.isoformat(),
            'aggregate_id': str(self.aggregate_id),
            'aggregate_type': self.aggregate_type,
            'data': self.data,
            'metadata': self.metadata,
        }

    def to_json(self):
        """Convert event to JSON string."""
        return json.dumps(self.to_dict(), default=str)


class EventHandler:
    """Base class for event handlers."""

    def handle(self, event: DomainEvent) -> None:
        """Handle the event."""
        raise NotImplementedError("Subclasses must implement handle()")


class EventDispatcher:
    """
    Central event dispatcher for the application.
    Supports synchronous and asynchronous event handling.
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """Singleton pattern implementation."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(EventDispatcher, cls).__new__(cls)
                    cls._instance._handlers = {}
                    cls._instance._async_handlers = {}
                    cls._instance._middleware = []
                    cls._instance._event_store = None
        return cls._instance

    def register_handler(self, event_type: str, handler: Callable, async_mode: bool = False) -> None:
        """
        Register a handler for a specific event type.

        Args:
            event_type: The type of event to handle
            handler: The handler function or class
            async_mode: Whether to handle asynchronously
        """
        handlers = self._async_handlers if async_mode else self._handlers

        if event_type not in handlers:
            handlers[event_type] = []

        if callable(handler):
            handlers[event_type].append(handler)
        elif isinstance(handler, EventHandler):
            handlers[event_type].append(handler.handle)
        else:
            raise ValueError("Handler must be callable or an EventHandler instance")

        logger.debug(f"Registered handler for event type: {event_type}")

    def register_middleware(self, middleware: Callable) -> None:
        """
        Register middleware that processes events before they are dispatched.
        """
        self._middleware.append(middleware)

    def dispatch(self, event: DomainEvent) -> None:
        """
        Dispatch an event to all registered handlers.
        """
        # Apply middleware
        for middleware in self._middleware:
            try:
                event = middleware(event)
                if event is None:
                    logger.warning(f"Event filtered by middleware: {event.event_type}")
                    return
            except Exception as e:
                logger.error(f"Middleware error for event {event.event_type}: {str(e)}")
                return

        # Store event if event store is configured
        if self._event_store:
            try:
                self._event_store.store(event)
            except Exception as e:
                logger.error(f"Failed to store event {event.event_type}: {str(e)}")

        # Dispatch to synchronous handlers
        self._dispatch_sync(event)

        # Dispatch to asynchronous handlers
        self._dispatch_async(event)

    def _dispatch_sync(self, event: DomainEvent) -> None:
        """Dispatch event to synchronous handlers."""
        handlers = self._handlers.get(event.event_type, [])
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                logger.error(f"Error in sync handler for {event.event_type}: {str(e)}")

    def _dispatch_async(self, event: DomainEvent) -> None:
        """Dispatch event to asynchronous handlers."""
        handlers = self._async_handlers.get(event.event_type, [])
        if not handlers:
            return

        # Use threading for simple async handling
        # Could be replaced with Celery or other task queue
        def async_wrapper():
            for handler in handlers:
                try:
                    handler(event)
                except Exception as e:
                    logger.error(f"Error in async handler for {event.event_type}: {str(e)}")

        thread = threading.Thread(target=async_wrapper)
        thread.daemon = True
        thread.start()

    def set_event_store(self, event_store) -> None:
        """Set the event store for persisting events."""
        self._event_store = event_store

    def clear_handlers(self) -> None:
        """Clear all registered handlers (useful for testing)."""
        self._handlers.clear()
        self._async_handlers.clear()
        self._middleware.clear()
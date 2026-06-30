"""
Event handlers for domain events.
"""

import logging
from .dispatcher import DomainEvent, EventHandler

logger = logging.getLogger(__name__)


class LoggingEventHandler(EventHandler):
    """
    Handler that logs events.
    """

    def handle(self, event: DomainEvent) -> None:
        """Log the event."""
        logger.info(f"Event: {event.event_type} - {event.aggregate_id}")


class AuditEventHandler(EventHandler):
    """
    Handler that logs events to the audit log.
    """

    def handle(self, event: DomainEvent) -> None:
        """Log the event to audit log."""
        audit_logger = logging.getLogger('audit')
        audit_logger.info(f"AUDIT: {event.event_type} - {event.to_json()}")
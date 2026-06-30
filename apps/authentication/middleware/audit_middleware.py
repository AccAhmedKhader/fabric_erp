"""
Audit middleware for logging requests and performance.
"""

import logging
from django.utils import timezone

logger = logging.getLogger(__name__)


class AuditMiddleware:
    """
    Middleware that logs requests and performance metrics.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = timezone.now()

        response = self.get_response(request)

        duration = (timezone.now() - start_time).total_seconds()

        if duration > 1.0:
            logger.warning(
                f"Slow request: {request.path} - {duration:.2f}s - "
                f"User: {request.user.username if request.user.is_authenticated else 'Anonymous'}"
            )

        if request.user.is_authenticated:
            logger.debug(
                f"Request: {request.method} {request.path} - "
                f"User: {request.user.username}"
            )

        return response
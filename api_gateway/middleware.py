from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Logs each request method, path, user, and timestamp.
    """

    def process_request(self, request):
        user = getattr(request, "user", None)
        logger.info(
            f"[{timezone.now()}] {request.method} {request.get_full_path()} "
            f"user: {getattr(user, 'email', 'anonymous')}"
        )


class SimpleRateLimitMiddleware(MiddlewareMixin):
    """
    Simple per-IP rate limiting (example).
    Note: For production, use Redis-based solution for distributed apps.
    """
    RATE_LIMIT = 100  # max requests
    TIME_WINDOW = 60  # seconds
    cache = {}

    def process_request(self, request):
        ip = self.get_client_ip(request)
        now = timezone.now().timestamp()

        history = self.cache.get(ip, [])
        history = [t for t in history if now - t < self.TIME_WINDOW]

        if not history:
            self.cache.pop(ip, None)

        if len(history) >= self.RATE_LIMIT:
            from django.http import JsonResponse
            return JsonResponse(
                {
                    "success": False,
                    "error": {
                        "type": "Throttled",
                        "code": "throttled",
                        "message": "Rate limit exceeded.",
                        "details": {"ip": ip},
                    },
                },
                status=429,
            )

        history.append(now)
        self.cache[ip] = history

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

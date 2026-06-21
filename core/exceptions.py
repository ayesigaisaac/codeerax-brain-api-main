from __future__ import annotations

from typing import Any

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def _normalize_error_details(details: Any) -> Any:
    if isinstance(details, dict):
        return {str(key): _normalize_error_details(value) for key, value in details.items()}

    if isinstance(details, list):
        return [_normalize_error_details(item) for item in details]

    return str(details)


def _extract_primary_message(details: Any) -> str:
    if isinstance(details, dict):
        for value in details.values():
            return _extract_primary_message(value)
        return "Request failed."

    if isinstance(details, list):
        return _extract_primary_message(details[0]) if details else "Request failed."

    return str(details)


def structured_exception_handler(exc: Exception, context: dict) -> Response | None:
    response = exception_handler(exc, context)

    if response is None:
        debug_details = str(exc) if settings.DEBUG else None
        return Response(
            {
                "success": False,
                "error": {
                    "type": exc.__class__.__name__,
                    "code": "server_error",
                    "message": "An unexpected server error occurred.",
                    "details": debug_details,
                },
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    normalized_details = _normalize_error_details(response.data)
    message = _extract_primary_message(normalized_details)
    default_code = getattr(exc, "default_code", "error")

    response.data = {
        "success": False,
        "error": {
            "type": exc.__class__.__name__,
            "code": str(default_code),
            "message": message,
            "details": normalized_details,
        },
    }
    return response

import hmac

from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import APIException, PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .schemas import HeartExecuteSchema
from .serializers import HeartExecuteSerializer
from .services import execute_internal_task, get_runtime


class ServiceUnavailable(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = "Service is currently unavailable."
    default_code = "service_unavailable"


class HeartExecuteView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        internal_token = getattr(settings, "HEART_INTERNAL_TOKEN", "").strip()
        request_token = request.headers.get("X-Internal-Token", "").strip()
        should_enforce_token = bool(internal_token) or not settings.DEBUG

        if should_enforce_token and not internal_token:
            raise ServiceUnavailable(
                "Server misconfiguration: HEART_INTERNAL_TOKEN is required."
            )

        if should_enforce_token and not request_token:
            raise PermissionDenied("X-Internal-Token header is required.")

        if should_enforce_token and not hmac.compare_digest(request_token, internal_token):
            raise PermissionDenied("Invalid internal token.")

        serializer = HeartExecuteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        schema = HeartExecuteSchema(**serializer.validated_data)
        data = execute_internal_task(schema)

        return Response(data, status=status.HTTP_202_ACCEPTED)


class HeartExecuteAliasView(HeartExecuteView):
    schema = None


class RuntimeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, project_id):
        data = get_runtime(project_id)
        return Response(data, status=status.HTTP_200_OK)


class RuntimeAliasView(RuntimeView):
    schema = None


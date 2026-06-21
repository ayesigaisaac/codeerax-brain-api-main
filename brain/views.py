from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .heart_client import get_heart_connection_info
from .schemas import BrainBuildSchema
from .serializers import BrainBuildSerializer
from .services import build_project
from .serializers import AuthEngineBuildSerializer
from .build_store import get_task


class BrainHealthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        heart = get_heart_connection_info()
        warnings = []

        if heart["mode"] == "external" and not heart["token_configured"]:
            warnings.append(
                "HEART_INTERNAL_TOKEN is not configured while external Heart dispatch is enabled."
            )

        return Response(
            {
                "status": "ok",
                "service": "brain",
                "heart_connection": heart,
                "warnings": warnings,
            },
            status=status.HTTP_200_OK,
        )


class BrainBuildView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = BrainBuildSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        schema = BrainBuildSchema(**serializer.validated_data)
        data = build_project(schema)
        if data.get("status") == "failed":
            return Response(data, status=status.HTTP_502_BAD_GATEWAY)

        return Response(data, status=status.HTTP_202_ACCEPTED)


class BrainAuthBuildView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AuthEngineBuildSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated = serializer.validated_data

        # Build a BrainBuildSchema that uses the generic build flow but forces the auth engine
        schema = BrainBuildSchema(
            prompt=validated.get("app_name") or "Build Auth Engine",
            project_id=validated.get("project_id"),
            user_id=validated.get("user_id"),
            feature="auth",
            requested_engine="auth",
            metadata={
                "app_name": validated.get("app_name"),
                "theme": validated.get("theme"),
                "config": validated.get("config"),
            },
        )

        data = build_project(schema)
        if data.get("status") == "failed":
            return Response(data, status=status.HTTP_502_BAD_GATEWAY)

        return Response(data, status=status.HTTP_202_ACCEPTED)


class BuildStatusView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, task_id: str):
        task = get_task(task_id)
        if not task:
            return Response({"detail": "Task not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(task, status=status.HTTP_200_OK)


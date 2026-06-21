from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from engines.dashboard_engine.services.dashboard_service import (
    get_dashboard_data,
    get_dashboard_summary,
)


class DashboardView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        data = get_dashboard_data()
        return Response(data.__dict__, status=status.HTTP_200_OK)


class DashboardSummaryView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        data = get_dashboard_summary()
        return Response(data.__dict__, status=status.HTTP_200_OK)


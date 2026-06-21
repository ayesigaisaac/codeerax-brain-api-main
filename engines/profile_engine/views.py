from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from engines.auth_engine.utils.authentication import (
    IsAuthenticatedCustom,
    JWTAuthentication,
)

from .schemas import CreateProfileSchema, PublicProfileSchema, UpdateProfileSchema
from .serializers import CreateProfileSerializer, UpdateProfileSerializer
from .services import create_profile, get_my_profile, get_public_profile, update_profile


class CreateProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedCustom]

    def post(self, request):
        serializer = CreateProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        schema = CreateProfileSchema(**serializer.validated_data)
        data = create_profile(request.user, schema)

        return Response(data, status=status.HTTP_201_CREATED)


class MyProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedCustom]

    def get(self, request):
        data = get_my_profile(request.user)
        return Response(data, status=status.HTTP_200_OK)


class UpdateProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedCustom]

    def post(self, request):
        serializer = UpdateProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        schema = UpdateProfileSchema(**serializer.validated_data)
        data = update_profile(request.user, schema)

        return Response(data, status=status.HTTP_200_OK)


class PublicProfileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        schema = PublicProfileSchema(user_id=str(user_id))
        data = get_public_profile(schema)

        return Response(data, status=status.HTTP_200_OK)


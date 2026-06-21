from rest_framework import serializers


class CreateProfileSerializer(serializers.Serializer):
    display_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    headline = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    bio = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    phone_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    country = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    city = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    website = serializers.URLField(required=False, allow_blank=True, allow_null=True)
    github_url = serializers.URLField(required=False, allow_blank=True, allow_null=True)
    linkedin_url = serializers.URLField(required=False, allow_blank=True, allow_null=True)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    is_public = serializers.BooleanField(required=False)


class UpdateProfileSerializer(serializers.Serializer):
    display_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    headline = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    bio = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    phone_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    country = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    city = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    website = serializers.URLField(required=False, allow_blank=True, allow_null=True)
    github_url = serializers.URLField(required=False, allow_blank=True, allow_null=True)
    linkedin_url = serializers.URLField(required=False, allow_blank=True, allow_null=True)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    is_public = serializers.BooleanField(required=False)


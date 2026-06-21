from rest_framework import serializers


class BrainBuildSerializer(serializers.Serializer):
    prompt = serializers.CharField()
    project_id = serializers.CharField(required=False, allow_blank=False)
    user_id = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    feature = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    requested_engine = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    metadata = serializers.JSONField(required=False)


# Serializer for Brain -> Auth Engine build requests
class AuthEngineBuildSerializer(serializers.Serializer):
    app_name = serializers.CharField()
    theme = serializers.JSONField(required=False, allow_null=True)
    config = serializers.JSONField(required=False)
    project_id = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    user_id = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def validate_app_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("app_name must be a non-empty string")
        return value.strip()


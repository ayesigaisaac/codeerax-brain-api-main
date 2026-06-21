from rest_framework import serializers


class HeartExecuteSerializer(serializers.Serializer):
    project_id = serializers.CharField()
    user_id = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    feature = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    requested_engine = serializers.CharField()
    prompt = serializers.CharField()
    metadata = serializers.JSONField(required=False)


from django.db import models
from django.utils import timezone


class RuntimeProject(models.Model):
    project_id = models.CharField(max_length=64, unique=True, db_index=True)
    user_id = models.CharField(max_length=64, blank=True, null=True)
    feature = models.CharField(max_length=100, blank=True, null=True)
    requested_engine = models.CharField(max_length=50)
    prompt = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, default="pending")
    runtime_data = models.JSONField(default=dict, blank=True)
    heart_payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    last_executed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"RuntimeProject<{self.project_id}>"


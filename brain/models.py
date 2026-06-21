import uuid

from django.db import models


class BuildTask(models.Model):
    STATUS_QUEUED = "queued"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_COMPLETED = "completed"
    STATUS_FAILED = "failed"

    STATUS_CHOICES = [
        (STATUS_QUEUED, "Queued"),
        (STATUS_IN_PROGRESS, "In progress"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_FAILED, "Failed"),
    ]

    task_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    project_id = models.CharField(max_length=100)
    requested_engine = models.CharField(max_length=50, default="auth")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_QUEUED)
    progress = models.PositiveSmallIntegerField(default=0)
    progress_history = models.JSONField(default=list, blank=True)
    message = models.TextField(blank=True, default="")
    error_message = models.TextField(blank=True, default="")
    config = models.JSONField(default=dict, blank=True)
    engines = models.JSONField(default=list, blank=True)
    heart_status = models.CharField(max_length=20, blank=True, default="")
    runtime_url = models.CharField(max_length=255, blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["task_id"]),
            models.Index(fields=["project_id", "requested_engine"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.task_id} ({self.status})"
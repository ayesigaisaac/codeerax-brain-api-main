

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BuildTask",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "task_id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("project_id", models.CharField(max_length=100)),
                (
                    "requested_engine",
                    models.CharField(default="auth", max_length=50),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("queued", "Queued"),
                            ("in_progress", "In progress"),
                            ("completed", "Completed"),
                            ("failed", "Failed"),
                        ],
                        default="queued",
                        max_length=20,
                    ),
                ),
                ("progress", models.PositiveSmallIntegerField(default=0)),
                ("progress_history", models.JSONField(blank=True, default=list)),
                ("message", models.TextField(blank=True, default="")),
                ("config", models.JSONField(blank=True, default=dict)),
                ("engines", models.JSONField(blank=True, default=list)),
                ("heart_status", models.CharField(blank=True, default="", max_length=20)),
                ("runtime_url", models.CharField(blank=True, default="", max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddIndex(
            model_name="buildtask",
            index=models.Index(fields=["task_id"], name="brain_buildt_task_id_7c6ad0_idx"),
        ),
        migrations.AddIndex(
            model_name="buildtask",
            index=models.Index(
                fields=["project_id", "requested_engine"],
                name="brain_buildt_project_3f8c64_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="buildtask",
            index=models.Index(fields=["status"], name="brain_buildt_status_3b1bc9_idx"),
        ),
    ]

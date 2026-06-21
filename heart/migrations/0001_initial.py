# Generated manually for heart app

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="RuntimeProject",
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
                ("project_id", models.CharField(db_index=True, max_length=64, unique=True)),
                ("user_id", models.CharField(blank=True, max_length=64, null=True)),
                ("feature", models.CharField(blank=True, max_length=100, null=True)),
                ("requested_engine", models.CharField(max_length=50)),
                ("prompt", models.TextField()),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("status", models.CharField(default="pending", max_length=20)),
                ("runtime_data", models.JSONField(blank=True, default=dict)),
                ("heart_payload", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("last_executed_at", models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]


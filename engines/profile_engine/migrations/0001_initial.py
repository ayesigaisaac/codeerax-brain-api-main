# Generated manually for profile_engine

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("display_name", models.CharField(blank=True, max_length=120, null=True)),
                ("headline", models.CharField(blank=True, max_length=255, null=True)),
                ("bio", models.TextField(blank=True, null=True)),
                ("phone_number", models.CharField(blank=True, max_length=30, null=True)),
                ("country", models.CharField(blank=True, max_length=80, null=True)),
                ("city", models.CharField(blank=True, max_length=80, null=True)),
                ("website", models.URLField(blank=True, null=True)),
                ("github_url", models.URLField(blank=True, null=True)),
                ("linkedin_url", models.URLField(blank=True, null=True)),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                ("is_public", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]


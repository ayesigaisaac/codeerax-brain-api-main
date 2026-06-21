from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("brain", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="buildtask",
            name="error_message",
            field=models.TextField(blank=True, default=""),
        ),
    ]

# Generated by Django 4.2.3 on 2023-07-28 15:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0004_follow"),
    ]

    operations = [
        migrations.AlterField(
            model_name="follow",
            name="following",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="followings",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]

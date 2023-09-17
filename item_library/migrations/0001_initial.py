# Generated by Django 4.1.5 on 2023-02-12 18:07

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Item",
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
                ("title", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("value", models.PositiveIntegerField(default=0)),
                (
                    "rarity",
                    models.CharField(
                        choices=[
                            ("common", "Common"),
                            ("uncommon", "Uncommon"),
                            ("rare", "Rare"),
                            ("very_rare", "Very Rare"),
                            ("legendary", "Legendary"),
                        ],
                        max_length=9,
                    ),
                ),
                (
                    "date_created",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("last_modified", models.DateTimeField(auto_now=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]

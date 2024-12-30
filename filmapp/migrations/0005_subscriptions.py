# Generated by Django 5.1 on 2024-12-27 10:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("filmapp", "0004_subscribers"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Subscriptions",
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
                ("start_date", models.DateField(auto_now_add=True)),
                ("end_date", models.DateField()),
                (
                    "pid",
                    models.ForeignKey(
                        db_column="pid",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="filmapp.plans",
                    ),
                ),
                (
                    "uid",
                    models.ForeignKey(
                        db_column="uid",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]

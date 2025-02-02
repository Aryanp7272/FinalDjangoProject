# Generated by Django 5.0.6 on 2024-06-07 05:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmapp', '0002_film_views_alter_film_type'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='price',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='film',
            name='views',
            field=models.BigIntegerField(default=0, verbose_name='views'),
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fid', models.ForeignKey(db_column='fid', on_delete=django.db.models.deletion.CASCADE, to='filmapp.film')),
                ('uid', models.ForeignKey(db_column='uid', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

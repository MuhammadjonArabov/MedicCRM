# Generated by Django 4.2.11 on 2024-11-13 14:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='seller',
            name='score',
            field=models.BigIntegerField(blank=True, default=0, null=True, verbose_name='Score'),
        ),
        migrations.AlterField(
            model_name='notifications',
            name='text',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Text'),
        ),
    ]

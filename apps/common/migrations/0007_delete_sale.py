# Generated by Django 4.2.11 on 2024-10-03 12:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0006_alter_statuschangerequest_comment_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Sale',
        ),
    ]
# Generated by Django 4.2.16 on 2024-09-25 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_medicalsector_inn_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymenttype',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='payment_type/', verbose_name='Image'),
        ),
    ]

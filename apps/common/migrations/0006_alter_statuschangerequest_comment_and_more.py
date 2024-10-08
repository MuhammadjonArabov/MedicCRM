# Generated by Django 4.2.11 on 2024-09-30 11:52

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_calendar_created_at_alter_calendar_updated_at_and_more'),
        ('common', '0005_paymentmethod_created_at_paymentmethod_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statuschangerequest',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='status_change_requests_comment', to='user.comment', verbose_name='Comment'),
        ),
        migrations.AlterField(
            model_name='statuschangerequest',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='status_change_requests_customer', to='common.customer', verbose_name='Customer'),
        ),
        migrations.AlterField(
            model_name='statuschangerequest',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status_change_requests_seller', to='user.seller', verbose_name='Seller'),
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantity')),
                ('sale_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Sale Date')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='common.product', verbose_name='Product')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.seller', verbose_name='Seller')),
            ],
            options={
                'verbose_name': 'Sale',
                'verbose_name_plural': 'Sales',
            },
        ),
    ]

# Generated by Django 4.2.11 on 2024-11-13 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicalsector',
            name='location',
        ),
        migrations.AddField(
            model_name='customer',
            name='coming_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Coming at'),
        ),
        migrations.AddField(
            model_name='medicalsector',
            name='sub_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='medical_sub_location', to='common.sublocation', verbose_name='Sub Location'),
        ),
        migrations.AddField(
            model_name='sale',
            name='latitude',
            field=models.FloatField(blank=True, null=True, verbose_name='Latitude'),
        ),
        migrations.AddField(
            model_name='sale',
            name='longitude',
            field=models.FloatField(blank=True, null=True, verbose_name='Longitude'),
        ),
        migrations.AddField(
            model_name='sale',
            name='status',
            field=models.BooleanField(default=True, verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='statuschangerequest',
            name='medical_Sector',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='status_change_requests', to='common.medicalsector'),
        ),
        migrations.AddField(
            model_name='statuschangerequest',
            name='medical_Sector_status',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='Medical Sector Status'),
        ),
        migrations.AddField(
            model_name='sublocation',
            name='city',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='sub_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='common.sublocation', verbose_name='SubLocation'),
        ),
        migrations.AlterField(
            model_name='statuschangerequest',
            name='admin_response',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Admin Response'),
        ),
        migrations.AlterField(
            model_name='statuschangerequest',
            name='type',
            field=models.CharField(choices=[('customer', 'Customer'), ('comment', 'Comment'), ('sold', 'Sold'), ('medical_sector', 'Medical Sector')], default='comment', max_length=20, verbose_name='Type'),
        ),
    ]

# Generated by Django 5.2.4 on 2025-07-14 04:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OrderService', '0006_remove_purchaseorder_total_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaseorderinwardedlog',
            name='returned_at',
        ),
        migrations.RemoveField(
            model_name='salesorder',
            name='total_amount',
        ),
    ]

# Generated by Django 5.2.4 on 2025-07-31 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0002_invoice_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='processing_error',
            field=models.TextField(blank=True, null=True),
        ),
    ]

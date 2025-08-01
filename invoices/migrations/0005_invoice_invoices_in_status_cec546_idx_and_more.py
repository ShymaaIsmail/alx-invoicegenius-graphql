# Generated by Django 5.2.4 on 2025-08-01 12:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0004_alter_invoice_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddIndex(
            model_name='invoice',
            index=models.Index(fields=['status'], name='invoices_in_status_cec546_idx'),
        ),
        migrations.AddIndex(
            model_name='invoice',
            index=models.Index(fields=['uploaded_at'], name='invoices_in_uploade_415f53_idx'),
        ),
    ]

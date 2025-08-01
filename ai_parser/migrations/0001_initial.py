# Generated by Django 5.2.4 on 2025-07-25 22:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('invoices', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AIParsingJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('success', models.BooleanField(default=False)),
                ('parsed_fields', models.JSONField(blank=True, null=True)),
                ('error_message', models.TextField(blank=True, null=True)),
                ('invoice', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ai_parsing_job', to='invoices.invoice')),
            ],
        ),
    ]

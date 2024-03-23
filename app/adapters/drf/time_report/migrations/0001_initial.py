# Generated by Django 5.0.3 on 2024-03-23 08:20

import app.domain.entities.time_report
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(choices=[('IN', 'in'), ('OUT', 'out')], max_length=3)),
                ('status', models.CharField(choices=[('PENDING', 'pending'), ('APPROVED', 'approved'), ('REJECTED', 'rejected')], default=app.domain.entities.time_report.TimeReportStatus['PENDING'], max_length=10)),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

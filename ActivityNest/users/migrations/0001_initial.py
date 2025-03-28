# Generated by Django 5.1.6 on 2025-03-16 22:48

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
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=255, null=True)),
                ('department', models.CharField(choices=[('EXTC', 'EXTC'), ('IT', 'IT'), ('CSE', 'CSE'), ('CS', 'CS')], default='EXTC', max_length=10)),
                ('year', models.CharField(choices=[('SE', 'SE'), ('TE', 'TE'), ('BE', 'BE')], default='SE', max_length=10)),
                ('roles', models.CharField(choices=[('Teacher', 'Teacher'), ('Student', 'Student')], default='Student', max_length=20)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated by Django 5.1.6 on 2025-03-17 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_member_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='profile_picture',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]

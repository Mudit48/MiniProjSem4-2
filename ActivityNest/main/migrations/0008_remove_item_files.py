# Generated by Django 5.1.6 on 2025-03-06 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_item_files'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='files',
        ),
    ]

# Generated by Django 5.1.6 on 2025-03-06 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_rename_s_username_item_susername'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='files',
            field=models.JSONField(default=list),
        ),
    ]

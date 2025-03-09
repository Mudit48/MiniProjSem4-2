# Generated by Django 5.1.6 on 2025-03-01 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('category', models.CharField(choices=[('achievement', 'achievement'), ('placement', 'placement'), ('certificate', 'certificate')], max_length=100)),
                ('description', models.CharField(max_length=200)),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]

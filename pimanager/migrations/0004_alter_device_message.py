# Generated by Django 4.2.17 on 2025-03-01 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pimanager', '0003_device_interface_blank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
    ]

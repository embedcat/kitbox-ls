# Generated by Django 4.0.2 on 2023-09-05 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logserver', '0006_rename_last_ping_kitbox_add_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='kitbox',
            name='log_request',
            field=models.BooleanField(default=False),
        ),
    ]

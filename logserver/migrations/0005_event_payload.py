# Generated by Django 4.0.2 on 2022-03-23 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logserver', '0004_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='payload',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
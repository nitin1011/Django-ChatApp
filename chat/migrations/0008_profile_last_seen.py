# Generated by Django 2.2 on 2020-05-22 14:14

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='last_seen',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 22, 14, 14, 32, 869133, tzinfo=utc)),
        ),
    ]
# Generated by Django 2.2 on 2020-06-03 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_profile_last_seen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='last_seen',
            field=models.DateTimeField(),
        ),
    ]

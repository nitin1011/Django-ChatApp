# Generated by Django 2.2 on 2020-07-25 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0011_auto_20200725_0641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='img_content',
            field=models.ImageField(blank=True, null=True, upload_to='image_message'),
        ),
    ]

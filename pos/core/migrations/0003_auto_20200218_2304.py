# Generated by Django 3.0.3 on 2020-02-18 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200218_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.FileField(upload_to=''),
        ),
    ]

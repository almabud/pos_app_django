# Generated by Django 3.0.4 on 2020-05-09 02:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('investor', '0002_auto_20200509_0639'),
    ]

    operations = [
        migrations.AddField(
            model_name='shareholder',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='investhistory',
            name='share_holder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='investor_history', to='investor.ShareHolder'),
        ),
    ]

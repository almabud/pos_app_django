# Generated by Django 3.0.4 on 2020-04-27 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_auto_20200428_0249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariant',
            name='gsm',
            field=models.CharField(blank=True, choices=[('', '----'), ('25', 25), ('30', 30), ('40', 40), ('50', 50), ('60', 60), ('70', 70), ('80', 80), ('90', 90), ('100', 100), ('110', 110)], max_length=4, null=True),
        ),
    ]

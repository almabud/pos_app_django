# Generated by Django 3.0.4 on 2020-04-04 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0030_auto_20200404_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suppliertransaction',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supplier_transactions', to='product.ProductVariant'),
        ),
    ]

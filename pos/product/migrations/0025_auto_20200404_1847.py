# Generated by Django 3.0.4 on 2020-04-04 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0024_auto_20200404_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suppliertransaction',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='product_variant', to='product.Product'),
            preserve_default=False,
        ),
    ]

# Generated by Django 3.0.4 on 2020-04-03 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_auto_20200330_0203'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('mobile_no', models.IntegerField()),
                ('address', models.TextField(blank=True, null=True)),
                ('product_variant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.ProductVariant')),
            ],
        ),
    ]

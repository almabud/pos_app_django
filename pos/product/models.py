from django.db import models

# Create your models here.
from product.manager import ColorManager, ProductManager


class Size(models.Model):
    """The model of bags size"""
    size = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.size


class Category(models.Model):
    """The model of bags category"""
    category = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category


class Color(models.Model):
    """The model define the color of the products"""
    color = models.CharField(max_length=100, unique=True)
    objects = ColorManager()

    def __str__(self):
        return self.color


class Product(models.Model):
    """The model of bags"""
    product_name = models.CharField(max_length=100, unique=True)
    product_description = models.TextField(null=True, blank=True)

    objects = ProductManager()

    def __str__(self):
        return self.product_name


class ProductVariant(models.Model):
    GSM_CHOICES = [
        ('25', 25),
        ('30', 30),
        ('40', 40),
        ('50', 50),
        ('60', 60),
        ('70', 70),
        ('80', 80),
        ('90', 90),
        ('100', 100),
        ('110', 110)
    ]
    gsm = models.CharField(max_length=4, choices=GSM_CHOICES)
    bag_purchase_price = models.FloatField(default=0.0)
    marketing_cost = models.FloatField(default=0.0)
    vat = models.FloatField(default=0.0)
    profit = models.FloatField(default=0.0)
    transport_cost = models.FloatField(default=0.0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    color = models.ForeignKey('Color', related_name='product_color', on_delete=models.CASCADE)
    size = models.ForeignKey('Size', related_name='product_size', on_delete=models.CASCADE)
    stock_total = models.IntegerField(default=0)
    product = models.ForeignKey('Product', related_name='variant', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('color', 'size', 'product', 'gsm', 'category')

    def __str__(self):
        return self.product.product_name

# class ProductTransaction(models.Model):
#     """This model define product specific detail like size color and the quantity"""
#     size = models.ForeignKey(Size, on_delete=models.CASCADE)
#     color = models.ForeignKey(Color, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     total_product = models.IntegerField()
#     objects = ProductTransactionManager()
#
#     def __str__(self):
#         return self.product.product_name


# class Supplier(models.Model):
#     """This model define the supplier details"""
#     name = models.CharField(max_length=100)
#     mobile_no = models.IntegerField()
#     address = models.TextField(blank=True, null=True)
#
#
# class SupplerTransaction(models.Model):
#     """This model define the supplier specific  details"""
#     supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
#     size = models.ForeignKey(Size, on_delete=models.CASCADE)
#     color = models.ForeignKey(Color, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     supplies = models.IntegerField()
#     date = models.DateTimeField(auto_now_add=True)

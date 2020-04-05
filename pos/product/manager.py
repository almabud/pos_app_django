from django.core.exceptions import ValidationError
from django.db import models, DatabaseError, transaction
from django.db.models import Sum, Prefetch, F


class ColorManager(models.Manager):
    def create(self, **kwargs):
        """Create new color"""
        if 'color' not in kwargs:
            raise ValueError('Please input a color')
        kwargs['color'] = kwargs['color'].capitalize()
        color = self.model(**kwargs)
        color.save(using=self.db)
        return color

    def update(self, objects):
        """Update existing color"""
        if not isinstance(objects, self.model):
            raise ValueError('Please insert correct value.')
        if not objects.color:
            raise ValueError('Please insert correct value2.')
        objects.color = objects.color.capitalize()
        objects.save(using=self.db)
        return objects


class ProductManager(models.Manager):
    def get_all_product(self):
        from product.models import ProductVariant
        data = self.model.objects.all().prefetch_related(
            Prefetch("variant",
                     queryset=ProductVariant.objects.select_related('color', 'size', 'category').filter(
                         stock_total__gt=0), to_attr="product_variant")).annotate(
            total_stock=Sum('variant__stock_total'))
        return data

    @transaction.atomic
    def create_product(self, **fields):
        if 'new_product' in fields:
            product = self.model(**fields['new_product'])
            try:
                product.save(using=self._db)
            except DatabaseError as e:
                raise DatabaseError(e)

            fields['product'] = product
            del fields['new_product']

        if 'new_color' in fields:
            from product.models import Color
            color = Color.objects.create(color=fields['new_color'])
            fields['color'] = color
            del fields['new_color']

        if 'new_size' in fields:
            from product.models import Size
            size = Size.objects.create(size=fields['new_size'])
            fields['size'] = size
            del fields['new_size']

        if 'new_category' in fields:
            from product.models import Category
            category = Category.objects.create(category=fields['new_category'])
            fields['category'] = category
            del fields['new_category']

        if 'product' in fields:
            keys = [
                'product',
                'color',
                'size',
                'gsm',
                'category',
                'marketing_cost',
                'vat',
                'profit',
                'stock_total',
                'transport_cost',
                'bag_purchase_price'
            ]
        if 'supplier' not in fields or not fields['supplier']:
            raise ValueError("Supplier field can't be empty.")

        if all(key in fields and fields[key] for key in keys):
            from product.models import ProductVariant
            supplier = fields['supplier']
            del fields['supplier']
            product = ProductVariant(**fields)
            product.save(using=self.db)
            from product.models import SupplierTransaction
            supplier = SupplierTransaction(supplier=supplier, product=product, total_supplied=fields['stock_total'])
            supplier.save(using=self.db)
            return product
        else:
            raise ValueError(
                'Product name, color, size, gsm, category, marketing cost, vat, bag purchase price, transport cost, '
                'stock total, profit can\t be empty')

    # def get_single_product(self, id):
    #     return self.model.objects.filter(pk=id).prefetch_related(Prefetch(
    #         "variant",
    #         queryset=ProductVariant.objects.select_related('color', 'size').filter(stock_total__gt=0),
    #         to_attr="product_variant")).annotate(total_stock=Sum('variant__stock_total'))


class SupplierManager(models.Manager):
    def get_all_supplier(self):
        data = self.model.objects.all().prefetch_related('product_supplier') \
            .annotate(total_supplied=Sum('product_supplier__total_supplied'))
        return data


class SupplierTransactionManager(models.Manager):
    def get_all_supplier(self):
        data = self.model.objects.all()
        print(data)
        return data

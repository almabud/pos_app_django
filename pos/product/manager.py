from decimal import *

from django.core.exceptions import ValidationError
from django.db import models, DatabaseError, transaction
from django.db.models import Sum, Prefetch, F, When, Q, Value, Case, FloatField, QuerySet
from django.db.models.functions import Coalesce


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


class ProductQuerySet(QuerySet):
    def get_all_product(self):
        from product.models import ProductVariant
        return self.model.objects.all().prefetch_related(
            Prefetch("variant",
                     queryset=ProductVariant.objects.select_related('color', 'size', 'category')
                     .annotate(price=F('bag_purchase_price') + F('marketing_cost') + F('vat') + F('printing_cost')
                                     + F('transport_cost') + F('profit')), to_attr="product_variant")) \
            .annotate(total_stock=Sum('variant__stock_total'))


class ProductManager(models.Manager):
    def get_query_set(self):
        return ProductQuerySet(self.model, using=self.db)

    def get_all_product(self):
        return self.get_query_set().get_all_product().order_by('-variant__stock_total')

    def get_all_product_stock_filter(self):
        return self.get_query_set().get_all_product().filter(variant__stock_total__gt=0)

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
            .annotate(total_supplied=Coalesce(Sum('product_supplier__total_supplied'), Value(0)))
        return data


class SupplierTransactionManager(models.Manager):
    def get_all_supplier(self):
        data = self.model.objects.all()
        print(data)
        return data


class CustomerManger(models.Manager):
    def get_all_customer(self):
        data = self.model.objects.all().prefetch_related('order_customer', 'order_customer__ordered_item_order') \
            .annotate(total_item=Sum('order_customer__ordered_item_order__quantity'),
                      total_due=Case(
                          When(order_customer__is_paid=False,
                               then=Sum((F('order_customer__ordered_item_order__quantity')
                                         * F('order_customer__ordered_item_order__price_per_product'))
                                        * (Value(1) - (
                                       F('order_customer__ordered_item_order__discount_percent') / 100.00))
                                        ) - F('order_customer__paid_total')),
                          default=Value(0),
                          output_field=FloatField()
                      ))
        return data


class OrderManager(models.Manager):
    def get_all_order(self):
        data = self.model.objects.all().prefetch_related('ordered_items').select_related('customer', 'sold_by') \
            .annotate(total_item=Coalesce(Sum('ordered_items__quantity'), Value(0)),
                      total_billed=Sum(
                          (F('ordered_items__quantity') * F('ordered_items__price_per_product'))
                          * (Value(1) - (F('ordered_items__discount_percent') / 100.00)),
                          output_field=FloatField()),
                      total_due=Case(
                          When(is_paid=False,
                               then=Sum((F('ordered_items__quantity')
                                         * F('ordered_items__price_per_product'))
                                        * (Value(1) - (F('ordered_items__discount_percent') / 100.00))
                                        ) - F('paid_total')),
                          default=Value(0),
                          output_field=FloatField()
                      )).order_by('-total_due')
        return data

    @transaction.atomic
    def crate_new_order(self, order=None, items=None):
        if not order or not items:
            raise ValueError("Order && items are missing")
        """Save the new customer"""
        if 'customer' not in order:
            new_customer_data = {
                'customer_name': order['customer_name'],
                'customer_phone': order['customer_phone'],
                'customer_address': order['customer_address']
            }
            del order['customer_name'],
            del order['customer_phone'],
            del order['customer_address']
            from product.models import Customer
            try:
                new_customer = Customer(**new_customer_data)
                new_customer.save(using=self.db)
            except DatabaseError as e:
                raise DatabaseError(e)
            order['customer'] = new_customer

        """Save the new order"""
        try:
            new_order = self.model(**order)
            new_order.save(using=self.db)
        except DatabaseError as e:
            raise DatabaseError("Database technical issue")

        from product.models import OrderedItem
        from product.models import ProductVariant
        """Save the paid total to as history"""
        if order['paid_total'] is not 0 or order['paid_total']:
            try:
                from product.models import PaymentHistory
                new_payment = PaymentHistory(order=new_order, amount=order['paid_total'])
                new_payment.save(using=self.db)
            except DatabaseError as e:
                raise DatabaseError("Database technical issue")
        """Save the items of the order"""
        new_item_queryset = list(ProductVariant.objects.filter(id__in=[i['product'] for i in items]))
        new_item_list = [OrderedItem(
            product=new_item_queryset[i],
            price_per_product=items[i]['price_per_product'], discount_percent=items[i]['discount_percent'],
            quantity=items[i]['quantity'], order=new_order
        ) for i in range(len(items))]

        try:
            OrderedItem.objects.bulk_create(new_item_list)
        except DatabaseError as e:
            raise DatabaseError("Database technical issue")

        """Update the stock of the items"""
        for i in range(len(items)):
            new_item_queryset[i].stock_total = new_item_queryset[i].stock_total - items[i]['quantity']

        try:
            ProductVariant.objects.bulk_update(new_item_queryset, ['stock_total'])
        except DatabaseError as e:
            raise DatabaseError("Database technical issue")

        return new_order

from decimal import *

from django.core.exceptions import ValidationError
from django.db import models, DatabaseError, transaction
from django.db.models import Prefetch, F, When, Q, Value, Case, FloatField, QuerySet, ExpressionWrapper, Sum, Avg, \
    Count, IntegerField
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


class ProductManager(models.Manager):
    def get_all_product(self):
        from product.models import ProductVariant
        from product.models import OrderedItem
        data = self.model.objects.prefetch_related(
            Prefetch("variant",
                     queryset=ProductVariant.objects.select_related('color', 'size', 'category').prefetch_related(
                         'OrderedItem_variants',
                     )
                     .annotate(price=F('bag_purchase_price') + F('marketing_cost') + F('vat') + F('printing_cost')
                                     + F('transport_cost') + F('profit')).annotate(
                         total_order=Count('OrderedItem_variants')).order_by('-stock_total'),
                     to_attr="product_variant")) \
            .annotate(total_stock=Sum('variant__stock_total')).order_by('-total_stock')
        return data

    def get_all_product_stock_filter(self):

        from product.models import ProductVariant
        return self.model.objects.prefetch_related(
            Prefetch("variant",
                     queryset=ProductVariant.objects.select_related('color', 'size', 'category')
                     .annotate(price=F('bag_purchase_price') + F('marketing_cost') + F('vat') + F('printing_cost')
                                     + F('transport_cost') + F('profit')).filter(stock_total__gt=0).order_by('id'),
                     to_attr="product_variant")) \
            .annotate(total_stock=Sum('variant__stock_total'))

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
                'size',
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
                'Product name, size, category, marketing cost, vat, bag purchase price, transport cost, '
                'stock total, profit can\t be empty')

    def update_product(self, id, data):
        old_product = self.model.objects.get(id=id)
        old_product.product_name = data['product_name']
        old_product.product_description = data['product_description']
        try:
            old_product.save(using=self.db)
        except DatabaseError as e:
            raise DatabaseError("Database technical problem updating product")
        return old_product


class ProductVariantManager(models.Manager):
    def get_product_variant_details(self, id):
        from product.models import SupplierTransaction
        return self.model.objects.filter(id=id).select_related('size', 'color', 'category', 'product') \
            .prefetch_related(
            Prefetch('product_variant',
                     queryset=SupplierTransaction.objects.select_related('supplier').order_by('-date'),
                     to_attr='supplier_list'
                     )

        ).annotate(price=F('bag_purchase_price') + F('marketing_cost') + F('vat') + F('printing_cost')
                         + F('transport_cost') + F('profit')).first()

    @transaction.atomic
    def update_variant(self, id, form_data):
        old_variant = self.model.objects.get(id=id)
        for key, value in form_data.items():
            setattr(old_variant, key, value)

        try:
            old_variant.save(using=self.db)
        except DatabaseError as e:
            raise DatabaseError("In updating variant there is database technical problem.")
        return old_variant

    @transaction.atomic
    def add_new_stock(self, id, form_data):
        old_variant = self.model.objects.get(id=id)
        old_variant.stock_total = old_variant.stock_total + form_data['new_stock']
        from product.models import SupplierTransaction
        try:
            old_variant.save(using=self.db)
        except DatabaseError as e:
            raise DatabaseError("Adding new stock problem in database")
        try:
            supplier = SupplierTransaction(supplier=form_data['supplier'], product=old_variant,
                                           total_supplied=form_data['new_stock'])
            supplier.save(using=self.db)
        except DatabaseError as e:
            raise DatabaseError("Adding supplier info problem in database")
        return supplier

    @transaction.atomic
    def delete_variant(self, id):
        if id is None:
            raise ValueError("Id is required")
        try:
            self.model.objects.get(id=id).delete()
        except DatabaseError as e:
            raise DatabaseError("Technical problem to delete variant")
        return True


class SupplierManager(models.Manager):
    def get_all_supplier(self):
        data = self.model.objects.all().prefetch_related('product_supplier') \
            .annotate(total_supplied=Coalesce(Sum('product_supplier__total_supplied'), Value(0)))
        return data

    def get_supplier_details(self, id):
        from product.models import SupplierTransaction
        data = self.model.objects.filter(id=1).prefetch_related(
            Prefetch('product_supplier', queryset=SupplierTransaction.objects.select_related(
                'product', 'product__size', 'product__color', 'product__category', 'product__product').order_by(
                '-date'), to_attr='product_list')
        ).first()
        return data

    @transaction.atomic
    def update_supplier(self, id, data):
        if not id or not data:
            raise ValueError('This field is required')

        if all(key in data and data[key] for key in ['name', 'mobile_no', 'address']):
            try:
                old_supplier = self.model.objects.get(id=id)
                old_supplier.name = data['name']
                old_supplier.mobile_no = data['mobile_no']
                old_supplier.address = data['address']
                old_supplier.save(using=self.db)
            except DatabaseError as e:
                raise DatabaseError("Database technical problem")
        else:
            raise ValueError("name, mobile_no, address are required.")

        return old_supplier


class SupplierTransactionManager(models.Manager):
    def get_all_supplier(self):
        data = self.model.objects.all()
        return data


class CustomerManger(models.Manager):
    def get_all_customer(self):
        total_billed = self.model.objects.prefetch_related('order_customer', 'order_customer__ordered_items') \
            .aggregate(
            total_billed=Sum(
                (F('order_customer__ordered_items__quantity') * F('order_customer__ordered_items__price_per_product')) *
                (Value(1) - F('order_customer__ordered_items__discount_percent') / 100.00),
                output_field=FloatField()
            ),
            total_item=Sum(F('order_customer__ordered_items__quantity'), output_field=IntegerField())
        )

        data = self.model.objects.prefetch_related('order_customer', 'order_customer__ordered_items') \
            .annotate(
            total_due=ExpressionWrapper(
                Value(total_billed['total_billed']) - Sum(F('order_customer__paid_total'), output_field=FloatField()),
                output_field=FloatField()),
            total_item=Value(total_billed['total_item'], output_field=IntegerField())
        )

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

    def get_order_detail(self, order_id):
        from product.models import OrderedItem
        from product.models import PaymentHistory
        data = self.model.objects.filter(pk=order_id).prefetch_related(
            Prefetch('ordered_items',
                     queryset=OrderedItem.objects.annotate(
                         sub_total=ExpressionWrapper(F('quantity') * F('price_per_product'), output_field=FloatField()))
                     .select_related('product', 'product__product', 'product__category', 'product__color',
                                     'product__size'),
                     to_attr='items'
                     ),
            Prefetch('payment_history',
                     queryset=PaymentHistory.objects.select_related('received_by').order_by('-date'),
                     to_attr='order_payment_history'
                     )
        ).select_related(
            'customer', 'sold_by') \
            .annotate(
            total_item=Coalesce(Sum('ordered_items__quantity'), Value(0)),
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
            )).first()
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
        """Save the paid total as history"""
        if order['paid_total'] is not 0 or order['paid_total']:
            try:
                from product.models import PaymentHistory
                new_payment = PaymentHistory(order=new_order, amount=order['paid_total'], received_by=order['sold_by'])
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
            new_stock = new_item_queryset[i].stock_total - items[i]['quantity']
            new_item_queryset[i].stock_total = new_stock if new_stock >= 0 else 0

        try:
            ProductVariant.objects.bulk_update(new_item_queryset, ['stock_total'])
        except DatabaseError as e:
            raise DatabaseError("Database technical issue")

        return new_order

    @transaction.atomic
    def make_payment(self, order_id, amount, received_by):
        """This method is responsible for add new payment to payment history"""
        if not order_id or not amount or not received_by:
            raise ValueError("All field is required")
        order = self.model.objects.get(id=order_id)
        order.paid_total = order.paid_total + float(amount)
        try:
            order.save(using=self.db)
        except DatabaseError as e:
            raise DatabaseError("Database technical issue")

        try:
            from product.models import PaymentHistory
            new_payment = PaymentHistory(order=order, amount=amount, received_by=received_by)
            new_payment.save(using=self.db)
        except DatabaseError as e:
            raise DatabaseError("Database technical issue")
        return new_payment

    @transaction.atomic
    def delete_order(self, id):
        if id is None:
            raise ValueError("Id is required")
        try:
            self.model.objects.get(id=id).delete()
        except DatabaseError as e:
            raise DatabaseError("Technical problem to delete order")
        return True

from django.test import TestCase

from product.models import Category, Size, Color, Product, ProductTransaction


class ModelTests(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(category='D-Cut')
        self.size = Size.objects.create(size='12/14')
        self.color = Color.objects.create(color='Red')
        self.product = Product.objects.create(
            product_name="ABC Bag",
            gsm=25,
            bag_purchase_price=5.80,
            marketing_cost=0.40,
            vat=0.40,
            profit=1,
            transport_cost=0.20,
            category=self.cat
        )
        self.product_transaction = ProductTransaction.objects.create(
            size=self.size,
            color=self.color,
            product=self.product,
            total_product=30
        )

    def test_add_new_category(self):
        """Add new category to the database"""
        category = 'D-Cut'
        cat = Category.objects.create(category=category)
        self.assertEqual(cat.category, category)

    def test_add_new_size(self):
        """Add new size to the database"""
        size = '12/14'
        object2 = Size.objects.create(size=size)
        self.assertEqual(object2.size, size)

    def test_add_new_color(self):
        """Add new color to the database"""
        color = 'red'
        color_object = Color.objects.create(color=color)
        self.assertEqual(color_object.color, color.capitalize())

    def test_update_existing_color(self):
        """Check editing Color model"""
        color = 'red'
        updated_color = 'green'
        color_object = Color.objects.create(color=color)
        color_object.color = updated_color
        color_object2 = Color.objects.update(color_object)
        self.assertEqual(color_object2.color, updated_color.capitalize())
        self.assertEqual(color_object.id, color_object2.id)

    def test_create_new_product(self):
        """Check if creating new product is working or not"""
        self.assertEqual(self.product.product_name, "ABC Bag")

    def test_create_product_transaction(self):
        """Check product transaction table"""
        self.assertEqual(self.product_transaction.product.product_name, self.product.product_name)

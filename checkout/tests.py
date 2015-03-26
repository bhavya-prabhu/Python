import datetime
from decimal import *
from django.test import TestCase
from checkout.models import *

class ProductTestCase(TestCase):

	def setUp(self):
		Product.objects.create(product_name = "milk", price = 1.2)

	def test_product_str(self):
		milk = Product.objects.get(product_name = "milk")
		self.assertEqual(str(milk), "milk: 1.2p")

class PurchaseTestCase(TestCase):

	def setUp(self):

		getcontext().prec = 2

                Product.objects.create(product_name = "milk", price = 1.2)
                Product.objects.create(product_name = "bread", price = 0.8)

		self.purchase_empty_list = Purchase.objects.create(items_list = u"", timestamp = datetime.datetime.now())
		self.purchase_comma_list = Purchase.objects.create(items_list = u",,,", timestamp = datetime.datetime.now())
		self.purchase_bad_item_name_list = Purchase.objects.create(items_list = u"milk, milk, deceased_parrot", timestamp = datetime.datetime.now())

		self.purchase_single_item_list = Purchase.objects.create(items_list = u"bread", timestamp = datetime.datetime.now())
		self.purchase_multiple_items_list = Purchase.objects.create(items_list = u"milk, bread, bread, milk, milk", timestamp = datetime.datetime.now())

	def test_empty_purchase_list(self):
		with self.assertRaises(InvalidPurchaseException) as e:
			self.purchase_empty_list.total_price()
		self.assertEqual(e.exception.message, "List of items may not be empty")

	def test_commas_only(self):
                with self.assertRaises(InvalidPurchaseException) as e:
                        self.purchase_comma_list.total_price()
		self.assertEqual(e.exception.message, "Invalid item name  in list of items.")

	def test_bad_item_name(self):
		with self.assertRaises(InvalidPurchaseException) as e:
			self.purchase_bad_item_name_list.total_price()
		self.assertEqual(e.exception.message, "Invalid item name deceased_parrot in list of items.")

	def test_single_item(self):
		self.assertEqual(self.purchase_single_item_list.total_price(), 	Decimal('0.8'))

	def test_multiple_items(self):
		self.assertEqual(self.purchase_multiple_items_list.total_price(), Decimal('5.2'))

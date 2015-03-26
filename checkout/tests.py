"""

tests.py

Author: Beth Ginsberg

Unit tests for the checkout example

"""

import datetime
from decimal import *
from django.test import TestCase
from checkout.models import *

class ProductTestCase(TestCase):

	"""

	Unit tests for the Product class.

	"""

	def setUp(self):
	
		"""	
	
		Create a sample Product object.

		"""
	
		Product.objects.create(product_name = "carrots", price = 1.2)
		Product.objects.create(product_name = "soap", price = 2.5, discount_purchase = 1, discount_receive = 2)

	def test_product_str(self):

		"""

		Test that the __str__ method works as expected.

		"""
	
		carrots = Product.objects.get(product_name = "carrots")
		self.assertEqual(str(carrots), "carrots: 1.2p")

	def test_product_str_with_discount(self):

		"""

		Test the __str__ method with a discount applied.

		"""

		soap = Product.objects.get(product_name = "soap")
		self.assertEqual(str(soap), "soap: 2.5p Discount: 2 for the price of 1")

class PurchaseTestCase(TestCase):

	"""

	Unit tests for the Purchase class.

	"""

	def setUp(self):

		"""

		Instantiate all the objects we will need for tests.

		"""

		# First create some Products to use as reference.
                Product.objects.create(product_name = "milk", price = 1.2)
                Product.objects.create(product_name = "bread", price = 0.8)
		Product.objects.create(product_name = "spam", price = 3.2, discount_purchase = 1, discount_receive = 2)
		Product.objects.create(product_name = "eggs", price = 0.7, discount_purchase = 2, discount_receive = 3)

		# Invalid Purchase objects
		self.purchase_empty_list = Purchase.objects.create(items_list = u"", timestamp = datetime.datetime.now())
		self.purchase_comma_list = Purchase.objects.create(items_list = u",,,", timestamp = datetime.datetime.now())
		self.purchase_bad_item_name_list = Purchase.objects.create(items_list = u"milk, milk, deceased_parrot", timestamp = datetime.datetime.now())

		# Valid Purchase objects
		self.purchase_single_item_list = Purchase.objects.create(items_list = u"bread", timestamp = datetime.datetime.now())
		self.purchase_multiple_items_list = Purchase.objects.create(items_list = u"milk, bread, bread, milk, milk", timestamp = datetime.datetime.now())

		# Testing discounts
		self.purchase_single_item_discount_list = Purchase.objects.create(items_list = u"spam", timestamp = datetime.datetime.now())
		self.purchase_multiple_item_discount_list = Purchase.objects.create(items_list = u"spam, spam, spam, spam", timestamp = datetime.datetime.now())
		self.purchase_non_multiple_item_discount_list = Purchase.objects.create(items_list = u"spam, spam, spam", timestamp = datetime.datetime.now())
		self.purchase_mixed_discount_list = Purchase.objects.create(items_list = u"spam, spam, milk, eggs, eggs, eggs", timestamp = datetime.datetime.now())

	def test_empty_purchase_list(self):

		"""

		Empty purchase list raises the correct exception.

		"""

		with self.assertRaises(InvalidPurchaseException) as e:
			self.purchase_empty_list.total_price()
		self.assertEqual(e.exception.message, "List of items may not be empty")

	def test_commas_only(self):
		
		"""

		Badly formed item list raises the correct exception.

		"""

                with self.assertRaises(InvalidPurchaseException) as e:
                        self.purchase_comma_list.total_price()
		self.assertEqual(e.exception.message, "Invalid item name  in list of items.")

	def test_bad_item_name(self):

		"""

		Non-existent item raises the correct exception.

		"""

		with self.assertRaises(InvalidPurchaseException) as e:
			self.purchase_bad_item_name_list.total_price()
		self.assertEqual(e.exception.message, "Invalid item name deceased_parrot in list of items.")

	def test_single_item(self):

		"""

		Price correctly calculated for a single item.

		"""

		self.assertEqual(self.purchase_single_item_list.total_price(), 	Decimal('0.8'))

	def test_multiple_items(self):

		"""
	
		Price correctly calculated for multiple items.

		"""

		self.assertEqual(self.purchase_multiple_items_list.total_price(), Decimal('5.2'))

	def test_single_item_discount(self):

		"""

		Test that discount is applied correctly to purchase of a single item.

		"""

		self.assertEqual(self.purchase_single_item_discount_list.total_price(), Decimal('3.2'))

	def test_multiple_item_discount(self):

		"""

		Check that the discount is applied correctly for multiple purchases of the same item.

		"""

		self.assertEqual(self.purchase_multiple_item_discount_list.total_price(), Decimal('6.4'))

	def test_non_multiple_item_discount(self):

		"""

		Check that the discount is applied correctly when the number purchased is not a multiple of the discount offered.

		"""

		self.assertEqual(self.purchase_non_multiple_item_discount_list.total_price(), Decimal('6.4'))

	def test_mixed_discount(self):

		"""

		Check that discounts are applied correctly for a mixture of discounted and non-discounted items.

		"""

		self.assertEqual(self.purchase_mixed_discount_list.total_price(), Decimal('5.8'))

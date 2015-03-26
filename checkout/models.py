"""

models.py

Author: Beth Ginsberg

This module contains the Django models required for the Supermarket project.

"""

import math
from decimal import *
from django.db import models

class Product(models.Model):

	"""

	Model for the Product class, representing any type of item for sale.

	Attributes:
		product_name -- the name of the product
		price -- the price of the product
		discount_purchase -- in the case of a discount, the number of items needed to be purchased in order to apply the discount
		discount_receive -- in the case of a discount, the number of items received if discount_purchase items are bought

	"""

	product_name = models.CharField(max_length = 20, primary_key = True)
	price = models.DecimalField(max_digits = 10, decimal_places = 2)
	discount_purchase = models.IntegerField(blank = True, null = True, default = None)
	discount_receive = models.IntegerField(blank = True, null = True, default = None)

	def __str__(self):

		"""

		Returns a string representation of this Product object.

		"""
	 	result = self.product_name + ": " + str(self.price) + "p"
		if self.discount_purchase and self.discount_receive:
			result += " Discount: " + str(self.discount_receive) + " for the price of " + str(self.discount_purchase)

		return result

class InvalidPurchaseException(Exception):

	"""

	Exception class representing bad user input of a Purchase.

	"""

	pass

class Purchase(models.Model):

	"""

	Model of the Purchase class, representing the purchase of a collection of Products.

	Attributes:
		timestamp -- the date and time at which the purchase was made
		items_list -- a comma-separated string representing the items that were purchased.

	This class also determines the total price of the purchase.

	"""

	timestamp = models.DateTimeField(auto_now = False, auto_now_add = True,)
	items_list = models.CharField(max_length = 200)

	def count_per_item(self, list_of_items):

		"""

		Helper function that counts the number of times that each item occurs in a list.

		For example, given the list ["apple", "apple", "orange", "apple"], the output would be {"apple": 3, "orange": 1}

		Additionally, the function checks that each item in the list corresponds to the name of an existing Product object.

		Parameters:
		list_of_items -- a list of strings representing the names to count.

		Returns:
		A dictionary mapping the names of the items to the number of times in which they occur in the list.

		"""

		counts = {}
                for item in list_of_items:
                        if item in counts:
				# The item is there already, so increment the counter.
                                counts[item] += 1
                        else:
                                try:
                                        # Test whether the product of that name exists.
                                        Product.objects.get(product_name=item)
                                        counts[item] = 1
                                except:
					raise InvalidPurchaseException("Invalid item name " + item + " in list of items.")
		return counts

	def total_price(self):

		"""

		Calculates the price of the Purchase based on the items_list and the price per Product.

		Returns a Decimal representing the total price.
	
		"""
	
		if not self.items_list:
                        raise InvalidPurchaseException("List of items may not be empty")


		# Split the string representation into a list and count the number of each item in the list.
		counts = self.count_per_item(map(unicode.strip, self.items_list.split(',')))

		# Apply discounts by iterating through the list and reducing the number of items appropriately.
		for product in counts:
			product_object = Product.objects.get(product_name = product)
			if product_object.discount_purchase and product_object.discount_receive:
				# Need to cast to a float in order for the ceil() function to work in Python 2. This has been fixed in Python 3.
				counts[product] = math.ceil(float(counts[product]) / float(product_object.discount_receive)) * product_object.discount_purchase

		# Iterate over the list, multiplying the count of each item by its price and keeping a running total.	
		total = Decimal('0.0')
		for item_name in counts:
			total += Decimal(counts[item_name]) * Decimal(Product.objects.get(product_name=item_name).price)
		return total

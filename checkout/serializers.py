"""

serializers.py

Author: Beth Ginsberg

Provides serializers for the checkout exercise

"""

from checkout.models import Product, Purchase
from rest_framework import serializers


class ProductSerializer(serializers.HyperlinkedModelSerializer):

	"""

	Serializes the Product class.

	"""

	class Meta:
        	model = Product
        	fields = ('product_name', 'price')


class PurchaseSerializer(serializers.HyperlinkedModelSerializer):

	"""

	Serializes the Purchase class.

	"""

	class Meta:
        	model = Purchase
        	fields = ('timestamp', 'items_list', 'total_price')

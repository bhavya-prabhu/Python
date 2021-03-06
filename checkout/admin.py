"""

admin.py

Author: Beth Ginsberg

Django admin to provide a simple web interface

"""

from django.contrib import admin
from checkout.models import Product, Purchase

class PurchaseAdmin(admin.ModelAdmin):

	list_display = ('timestamp', 'items_list', 'total_price')

admin.site.register(Product)
admin.site.register(Purchase, PurchaseAdmin)

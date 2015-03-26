from django.shortcuts import render
from rest_framework import viewsets
from checkout.serializers import ProductSerializer, PurchaseSerializer
from checkout.models import Product, Purchase

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class PurchaseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer


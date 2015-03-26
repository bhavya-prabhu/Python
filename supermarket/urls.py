"""

urls.py

Adapted from http://www.django-rest-framework.org/tutorial/quickstart/

"""

from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from checkout import views

router = routers.DefaultRouter()
router.register(r'product', views.ProductViewSet)
router.register(r'purchase', views.PurchaseViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]


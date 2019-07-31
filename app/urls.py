from django.conf.urls import url, include
from rest_framework import routers
from .views import AppOrderListViewSet

urls = [
    url(r'^numer/api/orders',AppOrderListViewSet.as_view()),
]

from django.conf.urls import url, include
from rest_framework import routers
from .views import AppOrderListViewSet, AppWorkListViewSet, AppUserCreateViewSet

urls = [
    url(r'^numer/api/orders',AppOrderListViewSet.as_view()),
    url(r'^numer/api/work',AppWorkListViewSet.as_view()),
    url(r'^numer/api/valid',AppUserCreateViewSet.as_view()),
]

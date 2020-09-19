from django.conf.urls import url, include
from rest_framework import routers
from .views import AppOrderListViewSet, AppWorkListViewSet
from .views import AppOrderItemView

urls = [
    url(r'^numer/api/orders',AppOrderListViewSet.as_view()),
    url(r'^numer/api/work',AppWorkListViewSet.as_view()),
    url(r'^numer/api/service/(?P<id>[0-9]+)/$',AppOrderItemView.as_view()),
]

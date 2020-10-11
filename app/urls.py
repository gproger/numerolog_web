from django.conf.urls import url, include
from rest_framework import routers
from .views import AppOrderListViewSet, AppWorkListViewSet
from .views import AppOrderItemView
from .views import FileServeView
from .views import AppOrderItemShowUpdateURLView
from .views import AppOrderCreateView
from .views import AppOrderItemShowUpdateConfirmView
from .views import AppOrderItemShowUpdateFileUploadView
from .views import AppCheckExpertView


urls = [
    url(r'^numer/api/orders',AppOrderListViewSet.as_view()),
    url(r'^numer/api/order/create', AppOrderCreateView.as_view()),
    url(r'^numer/api/work',AppWorkListViewSet.as_view()),
    url(r'^numer/api/service/(?P<id>[0-9]+)/$',AppOrderItemView.as_view()),
    url(r'^numer/api/service/expert/$',AppCheckExpertView.as_view()),
    url(r'^numer/api/serviceurl/(?P<id>[0-9]+)/$', AppOrderItemShowUpdateURLView.as_view(), name='service_pay_view'),
    url(r'^numer/api/servicecurl/(?P<id>[0-9]+)/$', AppOrderItemShowUpdateConfirmView.as_view(), name='service_expert_confirm'),
    url(r'^numer/api/servicefurl/(?P<id>[0-9]+)/$', AppOrderItemShowUpdateFileUploadView.as_view(), name='service_expert_upload'),
    url('^privatefiles/(?P<pk>[0-9]+)/$', FileServeView.as_view(), name='file_download'),
]

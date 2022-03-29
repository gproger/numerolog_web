
from __future__ import unicode_literals

from django.conf.urls import url

from .views import Notification

urlpatterns = [
    url(r'^tcbnotification/(?P<id>[0-9]+)/$', Notification.as_view(), name='tinkoffWebHookUrl'),
]



from __future__ import unicode_literals

from django.conf.urls import url

from .views import SmsNotify

urlpatterns = [
    url(r'^smsnotify/', SmsNotify.as_view(), name='smsnotify'),
]

from __future__ import unicode_literals

from django.conf.urls import url

from .views import SmsNotify, SMSVerifyPhone, SMSTestCode

urlpatterns = [
    url(r'^smsnotify/', SmsNotify.as_view(), name='smsnotify'),
    url(r'^get_sms_code/', SMSVerifyPhone.as_view(),name='smsverifyphone'),
    url(r'^check_sms_code/', SMSTestCode.as_view(),name='smstestcode'),
]

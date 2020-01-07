from __future__ import unicode_literals


from .models import SMSSettings
from .models import NotifySMS
from .models import PhoneAuthSMS
from django.utils.crypto import get_random_string
from .smsc_api import SMSC

from datetime import datetime
import random

from django.template import Template, Context


class SendSMSAPI(object):
    _settings = None

    def __init__(self):
        self._settings = SMSSettings.objects.last()

    def get_auth_phone_text(self, code):
        t = Template(self._settings.code_text)
        c = Context({"code" : code})
        return t.render(c)

    def send_verify_sms(self, phone):
        # first - check if sms was sended for this phones

        auth_obj = PhoneAuthSMS.objects.filter(phone=phone)
        if auth_obj.count() != 0:
            # get first object from queryset
            auth_obj = auth_obj.first()
            # test if date sended - current date > 5 min - we can send new sms
            seconds_cnt = auth_obj.get_time_delta()
            print(seconds_cnt)
            if seconds_cnt < 300:
                return {'desc' : 'Wait few seconds', 'result' : -1}
        else:
            auth_obj = PhoneAuthSMS()
            auth_obj.phone = phone

        auth_obj.code = random.randrange(100000,1000000,1)
        auth_obj.text = self.get_auth_phone_text(auth_obj.code)
        print(auth_obj.text)
        smsc = SMSC()
        res = smsc.send_sms(phones=auth_obj.phone,message=auth_obj.text)
        if res[1] > "0":
            auth_obj.status = 1
        else:
            auth_obj.status = 0
        auth_obj.save()
        return {'result' : auth_obj.status}

    def test_verify_sms_code(self, phone, code):

        auth_obj = PhoneAuthSMS.objects.filter(phone=phone)
        if auth_obj.count() == 0:
            return {'desc' : 'SMS not sended', 'result' : -1}

        auth_obj = auth_obj.first()
        if int(code) == int(auth_obj.code):
            return {'desc' : 'Code OK', 'result' : 1}
        else:
            return {'desc' : 'Code Fail', 'result' : 0}

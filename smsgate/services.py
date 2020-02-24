from __future__ import unicode_literals


from .models import SMSSettings
from .models import NotifySMS
from .models import PhoneAuthSMS
from django.utils.crypto import get_random_string
from .smsc_api import SMSC
from utils.phone import get_phone

from datetime import datetime
from schoolform.models import SchoolAppForm
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

    def send_verify_sms(self, phone, info):
        # first - check if sms was sended for this phones
        phone = get_phone(phone)

        auth_obj = PhoneAuthSMS.objects.filter(phone=phone)
        if auth_obj.count() != 0:
            # get first object from queryset
            auth_obj = auth_obj.first()
            # test if date sended - current date > 5 min - we can send new sms
            seconds_cnt = auth_obj.get_time_delta()
            if seconds_cnt < 300:
                return {'desc' : 'Wait few seconds', 'result' : -1, 'value':seconds_cnt, 'error':'time'}
        else:
            auth_obj = PhoneAuthSMS()
            auth_obj.phone = phone
            if info is not None:
                auth_obj.type = info['type']
                auth_obj.t_id = info['id']

        auth_obj.code = random.randrange(100000,1000000,1)
        auth_obj.text = self.get_auth_phone_text(auth_obj.code)
        print(auth_obj.text)
        smsc = SMSC()
        res = smsc.send_sms(phones=auth_obj.phone,message=auth_obj.text)
        if res[1] > "0":
            auth_obj.status = 1
            auth_obj.save()
            return {'result' : auth_obj.status}
        else:
            desc_text = ''
            if res[1][1:] == '7':
                desc_text = "Неправильный формат номера телефона"
            if res[1][1:] == '8':
                desc_text = "Сообщение не может быть доставлено"
            if res[1][1:] == '6':
                desc_text = "Сообщение не может быть доставлено(запрещена отправка)"

            auth_obj.status = 0
            return {'result' : auth_obj.status, 'desc' : desc_text}


    def test_verify_sms_code(self, phone, code):

        phone = get_phone(phone)

        auth_obj = PhoneAuthSMS.objects.filter(phone=phone)
        if auth_obj.count() == 0:
            return {'desc' : 'SMS not sended', 'result' : -1}

        auth_obj = auth_obj.first()
        if int(code) == int(auth_obj.code):
            if auth_obj.type == 'school':
                s_obj = SchoolAppForm.objects.get(pk=auth_obj.t_id)
                s_obj.phone = phone
                s_obj.phone_valid = True
                s_obj.save()
            return {'desc' : 'Code OK', 'result' : 1, 'phone' : phone}
        else:
            return {'desc' : 'Code Fail', 'result' : 0}

    def send_sms(self, phone, message):
        phone = get_phone(phone)

        sms = SendedSMS()
        sms.phone = phone
        sms.text = message

        smsc = SMSC()
        res = smsc.send_sms(phones=sms.phone,message=sms.text)

        if res[1] > "0":
            sms.status = 1
            sms.save()
            return {'result' : sms.status}
        else:
            desc_text = ''
            if res[1][1:] == '7':
                desc_text = "Неправильный формат номера телефона"
            if res[1][1:] == '8':
                desc_text = "Сообщение не может быть доставлено"
            if res[1][1:] == '6':
                desc_text = "Сообщение не может быть доставлено(запрещена отправка)"

            sms.status = 0
            sms.save()
            return {'result' : sms.status, 'desc' : desc_text}

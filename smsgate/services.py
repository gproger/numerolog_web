from __future__ import unicode_literals


from .models import SMSSettings
from .models import NotifySMS
from .models import PhoneAuthSMS
from django.utils.crypto import get_random_string
from .smsc_api import SMSC
from utils.phone import get_phone

from datetime import datetime
from schoolform.models import SchoolAppForm
from events.models import Ticket
import random

from django.template import Template, Context


type_values = ('school','ticket','auth')

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
        type = None
        t_id = None

        if info is not None:
            type = info.get('type',None)
        
        if info is not None:
            t_id = info.get('id',None)

        if type is None:
            return {'desc' : 'Type not setted', 'result' : -2 }   
        elif type not in type_values:
            return {'desc' : 'Type incorrect', 'result' : -3 }   

        

        auth_obj = PhoneAuthSMS.objects.filter(phone=phone,type=type)

        if auth_obj.count() != 0:
            # get first object from queryset
            auth_obj = auth_obj.first()
            # test if date sended - current date > 5 min - we can send new sms
            seconds_cnt = auth_obj.get_time_delta()
            if seconds_cnt < 300 or phone == '+79119804655':
                return {'desc' : 'Wait few seconds', 'result' : -1, 'timer': 300-int(seconds_cnt), 'error':'time','length' : 6}
        else:
            auth_obj = PhoneAuthSMS()
            auth_obj.phone = phone


        auth_obj.code = random.randrange(100000,1000000,1)
        auth_obj.text = self.get_auth_phone_text(auth_obj.code)

        if type is not None:
            auth_obj.type = type
        
        if t_id is not None:    
            auth_obj.t_id = t_id

        smsc = SMSC()
        res = smsc.send_sms(phones=auth_obj.phone,message=auth_obj.text)
        if res[1] > "0":
            auth_obj.status = 1
            auth_obj.save()
            return {'result' : auth_obj.status, 'length' : 6, 'timer' : 300}
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


    def test_verify_sms_code(self, phone, code, type):

        phone = get_phone(phone)

        auth_obj = PhoneAuthSMS.objects.filter(phone=phone, type=type)
        if auth_obj.count() == 0:
            return {'desc' : 'SMS not sended', 'result' : -1}

        auth_obj = auth_obj.first()
        if int(code) == int(auth_obj.code):

            if auth_obj.type is not None:
                if auth_obj.type == 'school':
                    s_obj = SchoolAppForm.objects.get(pk=auth_obj.t_id)
                    if s_obj.phone_valid is not True:
                        s_obj.phone = phone
                        s_obj.phone_valid = True
                        s_obj.save()
                if auth_obj.type == 'ticket':
                    t_obj = Ticket.objects.get(pk=auth_obj.t_id)
                    if t_obj.phone_valid is not True:
                        t_obj.phone = phone
                        t_obj.phone_valid = True
                        t_obj.save()

            ### need add verification for this user by phone )))        
            ### need delete verification object for this sms code ->     
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

    def get_pay_notify_text(self, context):
        c = Context(context)
        t = Template(self._settings.client_st)
        return t.render(c)

    def send_pay_notify_smd(self, phone, context):
        phone = get_phone(phone)
        sms = NotifySMS()
        sms.phone = phone
        sms.text = self.get_pay_notify_text(context)

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


    def get_work_notify_text(self,context):
        c = Context(context)
        t = Template(self._settings.expert_notify)
        return t.render(c)




    def send_expert_pending_confirmation(self, phone, context):
        phone = get_phone(phone)
        sms = NotifySMS()
        sms.phone = phone
        sms.text = self.get_work_notify_text(context)
        smsc = SMSC()
        res = smsc.send_sms(phones=sms.phone, message=sms.text)

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

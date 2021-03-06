from __future__ import unicode_literals

import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.contrib import auth
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from utils.phone import get_phone

from users.serializers import UserInfoSerializer

from misago.users.serializers import AnonymousUserSerializer, AuthenticatedUserSerializer



import logging

from .services import SendSMSAPI
from users.services import createNewUser

class SmsNotify(View):
    pass


class SMSVerifyPhone(View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode())
        phone = data.get('phone',None)
        phone = get_phone(phone)
        info = data.get('info', None)

        if phone is None:
            return JsonResponse({'desc' : 'Не указан номер телефона'}, status=400)

        sms = SendSMSAPI()

        res = sms.send_verify_sms(phone, info)

        if res['result'] == 1:
            return JsonResponse({'desc' : 'На указанный номер телефона выслан код подтверждения','length' : res['length'],'timer' : res['timer']}, status=200)

        if res['result'] == -1:
            return JsonResponse({'desc' : 'Попробуйте сделать запрос позже', 'length' : res['length'],'timer' : res['timer']}, status=400)

        if res['result'] == -2:
            return JsonResponse({'desc' : 'Ошибка в запросе'}, status=400)

        if res['result'] == -3:
            return JsonResponse({'desc' : 'Ошибка в запросе'}, status=400)


        if res['result'] == 0:
            return JsonResponse({'desc' : res['desc']}, status=400)


        return JsonResponse({'desc' : 'Ошибка отсылки смс'}, status=500)




class SMSTestCode(View):

    def post(self, request, *args, **kwargs):

        data = json.loads(request.body.decode())
        phone = data.get('phone',None)
        phone = get_phone(phone)
        code = data.get('code',None)
        info = data.get('info',None)

        if info is None:
            return JsonResponse({'desc' : 'Нет информации о верифицируемом объекте'}, status=400)

        type = info.get('type', None)

        if type is None:
            return JsonResponse({'desc' : 'Нет информации о типе верифицируемом объекте'}, status=400)

        if phone is None:
            return JsonResponse({'desc' : 'Не указан номер телефона'}, status=400)


        if code is None:
            return JsonResponse({'desc' : 'Не указан код подтверждения'}, status=400)

        sms = SendSMSAPI()

        res = sms.test_verify_sms_code(phone,code,type)


        if type == 'auth' and res['result'] == 1:
            ## need to auth user
            user = authenticate(username=phone,phone=phone,password=code)
            print(user)

            if user is None:
                user = createNewUser(phone, request.user_ip)
                user = authenticate(username=phone,phone=phone,password=code)
                
            auth.login(request, user)
            user_s_data = AuthenticatedUserSerializer(user).data
            user_info_data = UserInfoSerializer(user.ninfo).data
            res.update(user_s_data)
            res.update({'ninfo' : user_info_data})
 
        if res['result'] == -1:
            return JsonResponse({'desc' : 'На данный номер не высылалось сообщений'}, status=400)

        if res['result'] == 0:
            return JsonResponse({'desc' : 'Указан некорректный номер'}, status=400)


        return JsonResponse(res, status=200)

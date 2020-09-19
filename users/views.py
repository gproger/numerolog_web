from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.contrib.auth import update_session_auth_hash
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse

from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect
# Create your views here.
from django.utils.crypto import get_random_string

from .serializers import UserInfoSerializer
from .serializers import UserOrdersSerializer
from .serializers import UserOrderTicketsListSerializer
from .serializers import UserOrderSchoolListSerializer
from .serializers import UserOrderCuratorListSerializer
from .serializers import UserOrderServicesListSerializer
from .serializers import UserOrderTicketSerializer
from .serializers import UserOrderSchoolSerializer
from .serializers import UserOrderCuratorSerializer
from .serializers import UserOrderServicesSerializer
from .serializers import UserWorkSerializer
from misago.users.serializers import AnonymousUserSerializer, AuthenticatedUserSerializer

from .models import UserInfo
import json


class UserInfoDetail(generics.RetrieveUpdateAPIView):
    serializer_class = UserInfoSerializer
    queryset = UserInfo.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_fields = []

    def get_object(self):
        user = self.request.user
        return user.ninfo

class UserInfoValidateTest(View):
    pass

class UserInfoValidateSend(View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode())
        email = data.get('email',None)
        email = email.replace(' ','')
        email = email.lower()

        if email is None:
            return JsonResponse({'desc' : 'Указан некорректный адрес электронной почты либо пользователь с таким адресом уже существует'}, status=400)

        if not request.user.is_authenticated:
            return JsonResponse({'desc' : 'Авторизуйтесь в системе'}, status=403)

        try:
       	    validate_email( email )
        except ValidationError:
            return JsonResponse({'desc' : 'Указан некорректный адрес электронной почты либо пользователь с таким адресом уже существует'}, status=400)

        email = "".join(email.split())
        
        users = get_user_model().objects.filter(email=email)
        if users.count() > 0:
            return JsonResponse({'desc' : 'Указан некорректный адрес электронной почты либо пользователь с таким адресом уже существует'}, status=400)
            
        
        userinfo = request.user.ninfo
        userinfo.email_temp = email
        userinfo.validating_email = True
        userinfo.save()

        userinfo.send_email_code()
        ser = UserInfoSerializer(userinfo)
        return JsonResponse(ser.data, status=200)



class UserInfoValidateTest(View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode())
        code = data.get('code',None)
        code = code.replace(' ','')


        if code is None:
            return JsonResponse({'desc' : 'Не указан код проверки'}, status=400)

        if not request.user.is_authenticated:
            return JsonResponse({'desc' : 'Авторизуйтесь в системе'}, status=403)


        userinfo = request.user.ninfo


        if userinfo.email_validation_code == int(code):
            userinfo.validating_email = False
            userinfo.email = userinfo.email_temp
            userinfo.email_temp = ''
            userinfo.email_valid = True
            userinfo.save()
            passwd = get_random_string(12)
            userinfo.user.set_password(passwd)
            userinfo.user.set_email(userinfo.email)
            userinfo.user.save()
            update_session_auth_hash(request, request.user)


            ### send for user email and password
            ser = AuthenticatedUserSerializer(userinfo.user)
            userinfo.send_new_user_passwd(passwd)
            return JsonResponse(ser.data, status=200)
        else:
            return JsonResponse({'desc' : 'Код некорректен, адрес электронной почты неподтвержден'}, status=400)


class UserOrderTicketList(generics.ListAPIView):

    serializer_class = UserOrderTicketsListSerializer
    queryset = UserInfo.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        userInfo = self.request.user.ninfo
        if userInfo is not None:
            qs = userInfo.ticket_set.all()
            return qs
        return None


class UserOrderSchoolList(generics.ListAPIView):
    
    serializer_class = UserOrderSchoolListSerializer
    queryset = UserInfo.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        userInfo = self.request.user.ninfo
        if userInfo is not None:
            qs = userInfo.schoolappform_set.all()
            return qs
        return None


class UserOrderCuratorList(generics.ListAPIView):
    
    serializer_class = UserOrderCuratorListSerializer
    queryset = UserInfo.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        userInfo = self.request.user.ninfo
        if userInfo is not None:
            qs = userInfo.schoolappperscuratorform_set.all()
            return qs
        return None


class UserOrderList(generics.RetrieveUpdateDestroyAPIView):
    
    serializer_class = UserOrdersSerializer
    permission_classes = [IsAuthenticated]
    lookup_fields = []

    def get_object(self):
        user = self.request.user
        return user.ninfo


class UserWorksList(generics.RetrieveAPIView):

    serializer_clss = UserWorkSerializer
    permission_classes = [IsAuthenticated]
    lookup_fieds = []

    def get_objects(self):
        return self.request.user.serv_appl_doer


class UserOrderServicesList(generics.ListAPIView):
    pass


class UserOrderTicketDetail(generics.RetrieveAPIView):
    pass


class UserOrderSchoolDetail(generics.RetrieveAPIView):
    pass


class UserOrderCuratorDetail(generics.RetrieveAPIView):
    pass


class UserOrderServicesDetail(generics.RetrieveAPIView):
    pass

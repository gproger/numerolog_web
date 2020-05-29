from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.core.validators import email_re

from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect
# Create your views here.


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

from .models import UserInfo

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

        if email is None:
            return JsonResponse({'desc' : 'Не указан адрес электронной почты'}, status=400)

        if email_re.match(email):
            return JsonResponse({'desc' : 'Указан некорректный адрес электронной почты'}, status=400)

        if not request.user.IsAuthenticated:
            return JsonResponse({'desc' : 'Авторизуйтесь в системе'}, status=403)

        userinfo = request.user.ninfo
        userinfo.email_temp = email
        userinfo.validating_email = True
        userinfo.save()

        userinfo.send_email_code()

        return JsonResponse({'desc' : 'На указанный адрес электронной почты, выслан код подтерждения', 'length' : 6}, status=200)



class UserInfoValidateTest(View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode())
        code = data.get('code',None)

        if code is None:
            return JsonResponse({'desc' : 'Не указан код проверки'}, status=400)

        userinfo = request.user.ninfo

        if userinfo.email_validation_code == code:
            userinfo.validating_email = False
            userinfo.email = userinfo.email_temp
            userinfo.email_temp = ''
            userinfo.email_valid = True
            userinfo.save() 
            return JsonResponse({'desc' : 'Код корректен, адрес электронной почты подтвержден'}, status=200)
        else
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

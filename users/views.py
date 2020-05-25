from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
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

class UserInfoDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserInfoSerializer
    queryset = UserInfo.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_fields = []

    def get_object(self):
        user = self.request.user
        return user.ninfo


class UserOrderList(generics.RetrieveUpdateDestroyAPIView):
    
    serializer_class = UserOrdersSerializer
    permission_classes = [IsAuthenticated]
    lookup_fields = []

    def get_object(self):
        user = self.request.user
        return user.ninfo


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

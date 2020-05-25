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
from .serializers import UserOrderSerializer
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


class UserOrderList(generics.ListAPIView):
    pass


class UserOrderTicketList(generics.ListAPIView):
    pass


class UserOrderSchoolList(generics.ListAPIView):
    pass


class UserOrderCuratorList(generics.ListAPIView):
    pass


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

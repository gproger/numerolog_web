
from django.shortcuts import render
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, generics
from rest_framework.decorators import detail_route
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import *

from .serializers import AppOrderSerializer

class AppOrderListViewSet(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AppOrderSerializer

    def list(self, request):
        appUser = AppUser.objects.filter(email=request.user.email)
        if appUser.count() > 0:
            queryset = AppOrder.objects.filter(requester=appUser[0])
            serializer = AppOrderSerializer(queryset, many = True)
            return Response(serializer.data)
        else:
            raise Http404


# Create your views here.

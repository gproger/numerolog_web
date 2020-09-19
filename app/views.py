from django.http import Http404
from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied


from .models import AppOrder, AppResultFile

from .serializers import AppOrderSerializer, AppWorkSerializer
from .serializers import AppOrderItemExtSerializer
from private_storage.views import PrivateStorageDetailView


class AppOrderListViewSet(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = AppOrderSerializer

    def list(self, request):
        email = request.data.get('email').strip().lower()
        phone = request.data.get('phone').strip().lower()


class AppWorkListViewSet(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AppOrderSerializer

    def list(self, request):
        queryset = AppOrder.objects.filter(doer=request.user)
        serializer = AppWorkSerializer(queryset, many=True)
        return Response(serializer.data)


class AppOrderItemView(generics.RetrieveUpdateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = AppOrderItemExtSerializer

    def get_object(self):
        id = self.kwargs.get('id', None)

        return get_object_or_404(AppOrder,pk=id)

from pprint import pprint

class FileServeView(PrivateStorageDetailView):
    model=AppResultFile
    model_file_field='file'

    def can_access_file(self, private_file):
        obj = self.object
        if obj.order.owner.id == self.request.user.id:
            return True
        if obj.order.doer.id == self.request.user.id:
            return True
        return False

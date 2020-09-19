from django.http import Http404
from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied


from .models import AppOrder

from .serializers import AppOrderSerializer, AppWorkSerializer
from .serializers import AppOrderItemExtSerializer


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

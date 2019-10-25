from django.shortcuts import render
from django.http import Http404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import ServiceExpertSerializer, ServiceClientSerializer, ServiceExpertInfoSerializer
from .serializers import ServiceClientsCreateSerializer
from .models import ServiceExpert, ServiceClient

class ServiceExpertListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ServiceExpert.objects.all()

    serializer_class = ServiceExpertSerializer

class ServiceClientListView(generics.ListAPIView):
#    permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    serializer_class = ServiceClientSerializer

    def get_queryset(self):
        id = self.kwargs.get('id', None)
        obj = None
        if id is None:
            return ServiceClient.objects.none()
        try:
            obj = ServiceExpert.objects.get(id=id)
        except ServiceExpert.DoesNotExist:
            return ServiceClient.objects.none()
        return obj.clients

class ServiceExpertsClientListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
#    permission_classes = [AllowAny]

    serializer_class = ServiceClientSerializer

    def get_queryset(self):
        id = self.kwargs.get('id', None)
        obj = None
        if id is None:
            return ServiceClient.objects.none()
        try:
            obj = ServiceExpert.objects.get(id=id)
        except ServiceExpert.DoesNotExist:
            return ServiceClient.objects.none()
        return obj.clients

class ServiceExpertsClearBalanceView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ServiceClientSerializer
    
    def get(self,request,id):
        print(id)
        obj = ServiceExpert.objects.get(id=id)
        obj.balance = 0
        obj.save()
        return Response({},status=status.HTTP_200_OK)




class ServiceClientCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]    
    lookup_field = 'slug'

    def post(self, request, slug):
        id = self.kwargs.get('id', None)
        slug=self.kwargs.get('slug',None)
        c_exp = ServiceExpert.objects.filter(slug=slug)
        
        if c_exp.count() > 0:
            obj = c_exp.first()
            request.data.update({'expert' : obj.id})
        else:
            raise Http404
        
        ser = ServiceClientsCreateSerializer(data=request.data)
        print(request.data)
        if (ser.is_valid(raise_exception=True)):
            amount = int(request.data.get('amount'))
            if amount % 500 != 0:
                return Response({"amount" : "Некорректное значение"},status=status.HTTP_400_BAD_REQUEST)
            obj = ser.save()
            obj.create_payment(amount)
            return Response(ser.data)
# Create your views her

class ServiceExpertInfoView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    serializer_class = ServiceExpertInfoSerializer

    def get(self,request,slug):
        obj = ServiceExpert.objects.get(slug=slug)
        serializer = ServiceExpertInfoSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

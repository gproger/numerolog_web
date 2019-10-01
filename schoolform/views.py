from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model

from .models import SchoolAppForm, SchoolAppFlow

from .serializers import SchoolAppFormSerializer, SchoolAppFlowListSerializer
from .serializers import SchoolAppFlowSerializer, SchoolAppFlowWOChoicesSerializer
from django.shortcuts import render

# Create your views here.


class SchoolAppFormListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SchoolAppFormSerializer

    def get_queryset(self):
        query_params = self.request.query_params
        flow_num = query_params.get('flow', None)
        if flow_num == None:
            try:
                flow_num = SchoolAppFlow.objects.all().last()
            except SchoolAppFlow.DoesNotExist:
                return None
        else:
            try:
                flow_num = SchoolAppFlow.objects.get(flow=flow_num)
            except SchoolAppFlow.DoesNotExist:
                return None

        return SchoolAppForm.objects.all().filter(flow=flow_num)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = SchoolAppFormSerializer(queryset, many=True)
        return Response(serializer.data)


class SchoolAppFormCreateView(generics.CreateAPIView):
    serializer_class = SchoolAppFormSerializer
    queryset = SchoolAppForm.objects.all()
    permisiion_classes = [AllowAny]


class SchoolAppFlowListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SchoolAppFlowListSerializer

    def list(self, request):
        queryset = SchoolAppFlow.objects.all()
        serializer = SchoolAppFlowListSerializer(queryset, many=True)
        return Response(serializer.data)

class SchoolAppFlowView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SchoolAppFlowSerializer

    def get_object(self):
        id = self.kwargs.get('id', None)
        obj = None
        print(id)
        if id is None:
            return SchoolAppFlow.objects.none()
        try:
            obj = SchoolAppFlow.objects.get(flow=id)
        except SchoolAppFlow.DoesNotExist:
            obj = None

        return obj

class SchoolAppFlowRecruitmentListView(generics.ListAPIView):
    serializer_class = SchoolAppFlowWOChoicesSerializer
    queryset = SchoolAppFlow.objects.all().filter(state=1)
    permisiion_classes = [AllowAny]


class SchoolAppFormShowUpdateView(generics.RetrieveAPIView):
    
    serializer_class = SchoolAppFormSerializer
    permisiion_classes = [AllowAny]

    def get_object(self):
        id = self.kwargs.get('id', None)
        print(self.request)
        obj = None
        if id is None:
            return SchoolAppForm.objects.none()
        try:
            obj = SchoolAppForm.objects.get(pk=id)
        except SchoolAppForm.DoesNotExist:
            obj = None

        return obj


class SchoolAppFormShowUpdateURLView(generics.RetrieveAPIView):
    
    serializer_class = SchoolAppFormSerializer
    permisiion_classes = [AllowAny]

    def get_object(self):
        id = self.kwargs.get('id', None)
        print(self.request)
        obj = None
        if id is None:
            return SchoolAppForm.objects.none()
        try:
            obj = SchoolAppForm.objects.get(pk=id)
        except SchoolAppForm.DoesNotExist:
            obj = None

        obj.create_payment()

        return obj

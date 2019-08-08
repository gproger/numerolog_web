from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model

from .models import SchoolAppForm, SchoolAppFlow

from .serializers import SchoolAppFormSerializer, SchoolAppFlowSerializer
from django.shortcuts import render

# Create your views here.


class SchoolAppFormListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SchoolAppFormSerializer

    def get_queryset(self):
        query_params = self.request.query_params
        flow_num = query_params.get('flow', None)
        if flow_num == None:
            flow_num = SchoolAppFlow.objects.all().last()
        else:
            flow_num = SchoolAppFlow.objects.get(flow=flow_num)

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
    serializer_class = SchoolAppFlowSerializer

    def list(self, request):
        queryset = SchoolAppFlow.objects.all()
        serializer = SchoolAppFlowSerializer(queryset, many=True)
        return Response(serializer.data)


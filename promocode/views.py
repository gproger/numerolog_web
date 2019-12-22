from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied

from .serializers import PromoCodesSerializer
from .models import PromoCode
from schoolform.models import SchoolAppFlow
# Create your views here.


class PromoCodesListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PromoCodesSerializer


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
                flow_num = SchoolAppFlow.objects.get(id=flow_num)
            except SchoolAppFlow.DoesNotExist:
                return None

        return PromoCode.objects.all().filter(flow=flow_num)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = PromoCodesSerializer(queryset, many=True)
        return Response(serializer.data)

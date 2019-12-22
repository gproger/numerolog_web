from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied

from .serializers import PromoCodesSerializer
from .models import PromoCode
from schoolform.models import SchoolAppFlow
# Create your views here.
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.http import JsonResponse
from django.utils.crypto import get_random_string
import json

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


class PromoCodesCreate(LoginRequiredMixin, View):


    def post(self, request, *args, **kwargs):
        print(request)
        json_data = json.loads(request.body.decode('utf-8'))
        print(json_data)
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        if json_data['form']['codes_cnt'] <= 0:
            return JsonResponse({'desc' : 'Некорректное число кодов'}, status=400)

        if json_data['form']['elapsed_count'] <= 0:
            return JsonResponse({'desc' : 'Некорректное действия кода'}, status=400)

        flow = get_object_or_404(SchoolAppFlow,json_data['form']['flow'])

        for i in range(0,json['form']['codes_cnt']):
            code = get_random_string(12)
            pr = PromoCode()
            pr.code = code
            pr.discount = json_data['form']['discount']
            pr.is_percent = json_data['form']['is_percent']
            pr.flow = flow
            pr.emitter = request.user
            pr.elapsed_count = json_data['form']['elapsed_count']
            pr.save()

        return JsonResponse({'data' : 'created'}, status=201)

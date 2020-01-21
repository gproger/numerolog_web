from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.exceptions import PermissionDenied

from .serializers import PromoCodesSerializer
from .serializers import PromoCodesTicketSerializer
from .models import PromoCode
from schoolform.models import SchoolAppFlow
from events.models import EventTicketTemplate
# Create your views here.
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.http import JsonResponse
from django.utils.crypto import get_random_string
import json

class PromoCodesListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
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
        json_data = json.loads(request.body.decode('utf-8'))
        if not request.user.is_staff:
            return HttpResponseForbidden()

        if int(json_data['form']['codes_cnt']) <= 0:
            return JsonResponse({'desc' : 'Некорректное число кодов'}, status=400)

        if int(json_data['form']['elapsed_count']) <= 0:
            return JsonResponse({'desc' : 'Некорректное действия кода'}, status=400)

        flow = get_object_or_404(SchoolAppFlow,pk=json_data['form']['flow'])

        print(json_data)

        for i in range(0,int(json_data['form']['codes_cnt'])):
            code = get_random_string(12)
            while PromoCode.objects.filter(flow=flow,code=code).count() > 0:
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


class PromoCodesTest(View):


    def post(self, request, *args, **kwargs):
        print(request)
        json_data = json.loads(request.body.decode('utf-8'))

        flow = get_object_or_404(SchoolAppFlow,pk=json_data['flow'])
        code = PromoCode.objects.filter(flow=flow,code=json_data['code'], elapsed_count__gte=1)

        if code.count() == 0:
             return JsonResponse({'code': 'failed'}, status=404)
        else:
             return JsonResponse({'code': 'success','discount':code[0].discount,'is_percent':code[0].is_percent}, status=200)


class PromoTicketCodesTestTicket(View):

    def post(self, request, *args, **kwargs):
        print(request)
        json_data = json.loads(request.body.decode('utf-8'))

        event = get_object_or_404(EventTicketTemplate,pk=json_data['ev_id'])
        code = PromoCode.objects.filter(evticket=event,code=json_data['code'], elapsed_count__gte=1)

        if code.count() == 0:
             return JsonResponse({'code': 'failed'}, status=404)
        else:
             return JsonResponse({'code': 'success','discount':code[0].discount,'is_percent':code[0].is_percent}, status=200)


class PromoTicketCodesListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = PromoCodesTicketSerializer


    def get_queryset(self):
        query_params = self.request.query_params
        event = query_params.get('event', None)
        if event == None:
            try:
                event = EventTicketTemplate.objects.all().last()
            except EventTicketTemplate.DoesNotExist:
                return None
        else:
            try:
                event = EventTicketTemplate.objects.get(id=event)
            except EventTicketTemplate.DoesNotExist:
                return None

        return PromoCode.objects.all().filter(evticket=event)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = PromoCodesSerializer(queryset, many=True)
        return Response(serializer.data)



class PromoTicketCodesCreate(LoginRequiredMixin, View):


    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body.decode('utf-8'))
        if not request.user.is_staff:
            return HttpResponseForbidden()

        if int(json_data['form']['codes_cnt']) <= 0:
            return JsonResponse({'desc' : 'Некорректное число кодов'}, status=400)

        if int(json_data['form']['elapsed_count']) <= 0:
            return JsonResponse({'desc' : 'Некорректное действия кода'}, status=400)

        event = get_object_or_404(EventTicketTemplate,pk=json_data['form']['event'])

        print(json_data)

        for i in range(0,int(json_data['form']['codes_cnt'])):
            code = get_random_string(12)
            while PromoCode.objects.filter(evticket=event,code=code).count() > 0:
                code = get_random_string(12)

            pr = PromoCode()
            pr.code = code
            pr.discount = json_data['form']['discount']
            pr.is_percent = json_data['form']['is_percent']
            pr.evticket = event
            pr.emitter = request.user
            pr.elapsed_count = json_data['form']['elapsed_count']
            pr.save()

        return JsonResponse({'data' : 'created'}, status=201)

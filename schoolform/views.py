from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect

from .models import SchoolAppForm, SchoolAppFlow, SchoolAppCurator, PriceField, SchoolAppPersCuratorForm
from blog.models import TermsOfServicePage

from .serializers import SchoolAppFormSerializer, SchoolAppFlowListSerializer
from .serializers import SchoolAppFormCreateSerializer,SchoolAppFormFlowStudentsList
from .serializers import SchoolAppFlowSerializer, SchoolAppFlowWOChoicesSerializer, SchoolAppCuratorCreateSerializer
from .serializers import SchoolPersCuratorSerializer
from .serializers import SchoolAppFlowWOChoicesSerializerBySlug
from django.shortcuts import render, get_object_or_404
from promocode.models import PromoCode
from django_tinkoff_merchant.serializers import PaymentSerializer
import json

from django.http import JsonResponse
from datetime import datetime, timezone


# Create your views here.


class SchoolAppFormListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
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
                flow_num = SchoolAppFlow.objects.get(id=flow_num)
            except SchoolAppFlow.DoesNotExist:
                return None

        return SchoolAppForm.objects.all().filter(flow=flow_num)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = SchoolAppFormFlowStudentsList(queryset, many=True)
        return Response(serializer.data)

class SchoolAppFormCreateView(generics.CreateAPIView):
    serializer_class = SchoolAppFormCreateSerializer
    queryset = SchoolAppForm.objects.all()
    permission_classes = [IsAuthenticated]

    def post(cls, request, format=None):
        ser = SchoolAppFormCreateSerializer(data=request.data)
        if (ser.is_valid(raise_exception=True)):
            cc_flow = request.data.get('flow_id')
            cc_code = request.data.get('code', None)
            c_flow = get_object_or_404(SchoolAppFlow,id=cc_flow)
            if c_flow.state != 1:
                raise PermissionDenied({"message":"Запись на этот поток/курс не активна" })

            code = None

            if cc_code is not None:
                code = PromoCode.objects.filter(flow=c_flow,
                                                code=cc_code,
                                                elapsed_count__gte=1)

            if c_flow.avail_by_code:
                if code.count() <= 0:
                    raise PermissionDenied({"message":
                                     "Код для записи на курс не корректен" })



            objs = SchoolAppForm.objects.filter(flow=c_flow,email=request.data.get('email').strip().lower())
            if objs.count() > 0:
                objs = objs.first()
                ser = SchoolAppFormCreateSerializer(objs)
            else:
                objs = ser.save()
                if code is not None:
                    code_item = code[0]
                    pr_field = PriceField()
                    pr_field.price = objs.price
                    if code_item.is_percent:
                        pr_field.discount = pr_field.price*code_item.discount/100
                    else:
                        pr_field.discount = code_item.discount
                    objs.price = pr_field.price - pr_field.discount
                    pr_field.save()
                    objs.price_f = pr_field
                    objs.save()
                    code_item.price.add(pr_field)
                    code_item.elapsed_count = code_item.elapsed_count - 1
                    code_item.save()


            return Response(ser.data)

class SchoolAppCuratorCreateView(generics.CreateAPIView):
    serializer_class = SchoolAppCuratorCreateSerializer
    queryset = SchoolAppCurator.objects.all()
    permission_classes = [IsAuthenticated]

    def post(cls, request, format=None):
        ser = SchoolAppCuratorCreateSerializer(data=request.data)
        if (ser.is_valid(raise_exception=True)):
            cc_flow = request.data.get('flow_id')
            if cc_flow is None:
                cc_flow=5
            c_flow = get_object_or_404(SchoolAppFlow,id=cc_flow)
            if c_flow.state == 0 or c_flow.state == 4:
                raise PermissionDenied({"message":"Запись на этот поток/курс не активна" })
            objs = SchoolAppCurator.objects.filter(flow=c_flow,email=request.data.get('email').strip().lower())
            if objs.count() > 0:
                objs = objs.first()
                ser = SchoolAppCuratorCreateSerializer(objs)
            else:
                objs = ser.save()
            return Response(ser.data)


class SchoolAppFlowListView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = SchoolAppFlowListSerializer

    def list(self, request):
        queryset = SchoolAppFlow.objects.all()
        serializer = SchoolAppFlowListSerializer(queryset, many=True)
        return Response(serializer.data)

class SchoolAppFlowView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = SchoolAppFlowSerializer

    def get_object(self):
        id = self.kwargs.get('id', None)

        return get_object_or_404(SchoolAppFlow,pk=id)

class SchoolAppFlowRecruitmentListView(generics.ListAPIView):
    serializer_class = SchoolAppFlowWOChoicesSerializer
    startdate = datetime.today()
    queryset = SchoolAppFlow.objects.all().filter(state=1,is_hidden=False, recruitment_stop__gt=startdate)
    permission_classes = [AllowAny]


class SchoolAppFlowViewBySlug(generics.RetrieveAPIView):
    serializer_class = SchoolAppFlowWOChoicesSerializerBySlug
    queryset = SchoolAppFlow.objects.all()
    lookup_field = 'slug'
    permission_classes = [AllowAny]

    def get_objects(self):
        slug = self.kwargs.get('slug',None)
        print('Search for slug ' + slug)
        return get_object_or_404(SchoolAppFlow,slug=slug)


class SchoolAppFlowRegisterListView(generics.ListAPIView):
    serializer_class = SchoolAppFlowWOChoicesSerializer
    queryset = SchoolAppFlow.objects.all().filter(state=2,is_hidden=False)
    permission_classes = [AllowAny]


class SchoolAppFormShowUpdateView(generics.RetrieveAPIView):

    serializer_class = SchoolAppFormSerializer
    permisiion_classes = [IsAuthenticated]

    def get_object(self):

        id = self.kwargs.get('id', None)

        return get_object_or_404(SchoolAppForm,pk=id)


    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        email = request.GET.get('email', None)
        if email is None:
             raise PermissionDenied({"message":"У вас нет прав доступа для просмотра данных" })
        if email.lower() != obj.email.lower():
             raise PermissionDenied({"message":"У вас нет прав доступа для просмотра данных" })

        return super(SchoolAppFormShowUpdateView,self).get(request,*args,**kwargs)


class SchoolAppFormShowUpdateURLView(generics.UpdateAPIView):

    serializer_class = SchoolAppFormSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        id = self.kwargs.get('id', None)

        return get_object_or_404(SchoolAppForm,pk=id)

    def put(self, request, *args, **kwargs):
        inst = self.get_object()

        if request.data['amount']  <= 0:
            return Response({"amount" : "Интересная попытка :)"},status=status.HTTP_400_BAD_REQUEST)
#        if request.data['amount'] % 100000 != 0:
#            return Response({"amount" : "Некорректное значение"},status=status.HTTP_400_BAD_REQUEST)
        if request.data['amount'] > inst.price*100:
            return Response({"amount" : "Введенная сумма слишком велика"},status=status.HTTP_400_BAD_REQUEST)


        total = 0
        for k in inst.payment.all():
            if k.status == 'CONFIRMED':
                total += k.amount

        if request.data['amount'] > inst.price*100-total:
            return Response({"amount" : "Введенная сумма слишком велика"},status=status.HTTP_400_BAD_REQUEST)

        inst.create_payment(amount=request.data['amount'])
        inst.save()

        return super(SchoolAppFormShowUpdateURLView,self).put(request,*args,**kwargs)

class SchoolPersCuratorPayView(generics.CreateAPIView):

    serializer_class = SchoolPersCuratorSerializer
    permission_classes = [IsAuthenticated]


class SchoolApplyPersCurator(View):
    def post(self, request, *args, **kwargs):

        json_data = json.loads(request.body.decode('utf-8'))
        flow = get_object_or_404(SchoolAppFlow,id=json_data['flow_id'])
        form = get_object_or_404(SchoolAppForm,id=json_data['form_id'])
        if flow != form.flow:
            return HttpResponseForbidden()

        cur = SchoolAppPersCuratorForm()
        cur.first_name = form.first_name
        cur.last_name = form.last_name
        cur.phone = form.phone
        cur.bid = form.bid
        cur.middle_name = form.middle_name
        cur.email = form.email
        cur.flow = flow
        cur.price = flow.pers_cur_price
        test_c = True
        for term in json_data['accepted_toss']:
            tobj = get_object_or_404(TermsOfServicePage,id=term)
            if tobj not in flow.pers_cur_toss.all():
                test_c = False

        if not test_c:
            return HttpResponseBadRequest

        cur.save()

        for term in json_data['accepted_toss']:
            tobj = get_object_or_404(TermsOfServicePage,id=term)
            cur.accepted_toss.add(tobj)

        cur.save()
        paym = cur.payment.last()
        serializer = PaymentSerializer(paym)
        return JsonResponse(serializer.data)


class SchoolApplyPersCuratorGetPayURL(View):
    def get(self, request, *args, **kwargs):

        id = self.kwargs.get('id', None)
        print(id)
        pform = get_object_or_404(SchoolAppPersCuratorForm,pk=id)
        pform.create_payment()
        paym = pform.payment.last()
        serializer = PaymentSerializer(paym)
        return JsonResponse(serializer.data)


class SchoolAppFromFilterByPayDate(View):
    def get(self, request, *args, **kwargs):
        date = self.kwargs.get('date', None)
        dtime = datetime.strptime("24-8-2019 15:00:00","%d-%m-%Y %H:%M:%S")
        dt = datetime.strptime("24-8-2017 15:00:00","%d-%m-%Y %H:%M:%S").replace(tzinfo=timezone.utc)
        objs = SchoolAppForm.get_registered_from_date(dt)
        print(objs)

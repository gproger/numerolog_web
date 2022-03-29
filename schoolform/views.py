from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, BasePermission
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect

from .models import SchoolAppForm, SchoolAppFlow, SchoolAppCurator, PriceField, SchoolAppPersCuratorForm
from .models import SchoolExtendAccessService
from blog.models import TermsOfServicePage

from .serializers import SchoolAppFormSerializer, SchoolAppFlowListSerializer
from .serializers import SchoolAppFormCreateSerializer,SchoolAppFormFlowStudentsList
from .serializers import SchoolAppFlowSerializer, SchoolAppFlowWOChoicesSerializer, SchoolAppCuratorCreateSerializer
from .serializers import SchoolPersCuratorSerializer
from .serializers import SchoolAppFlowWOChoicesSerializerBySlug
from .serializers import SchoolPersCuratorListSerializer
from .serializers import SchoolCuratorListSerializer
from .serializers import SchoolAppDiscountListSerializer
from .serializers import SchoolAppDiscountCreateSerializer
from .serializers import SchoolExtendAccessServiceCreateSerializer
from .serializers import SchoolExtendAccessServiceSerializer
from .serializers import SchoolSaleFormSerializer
from .serializers import SchoolAppExtendFormListSerializer
from django.shortcuts import render, get_object_or_404
from promocode.models import PromoCode
from django_tinkoff_merchant.serializers import PaymentSerializer
import json
from private_storage.views import PrivateStorageDetailView


from django.http import JsonResponse
from datetime import datetime, timezone
from utils.phone import get_phone
from .models import SchoolScanFile
from .models import SchoolDiscount
from .models import SchoolExtendAccessService
from .models import SchoolAppFlow
from tinkoff_credit.models import *
from tinkoff_credit.service import *
from users.models import UserInfo
import locale

# Create your views here.

class IsSchoolAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        if not request.user.is_authenticated:
            return False

        return request.user.has_perm('schoolform.change_schoolappflow') or request.user.is_superuser


class SchoolAppFormListView(generics.ListAPIView):
    permission_classes = [IsSchoolAdmin]
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

class SchoolAppPersCuratorListView(generics.ListAPIView):
    permission_classes = [IsSchoolAdmin]
# dummy empty serializer for no additional params
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

        return SchoolAppPersCuratorForm.objects.all().filter(flow=flow_num)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = SchoolPersCuratorListSerializer(queryset, many=True)
        return Response(serializer.data)


class SchoolExtendListView(generics.ListAPIView):
    permission_classes = [IsSchoolAdmin]
# dummy empty serializer for no additional params
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

        return SchoolExtendAccessService.objects.all().filter(form__flow=flow_num)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = SchoolAppExtendFormListSerializer(queryset, many=True)
        return Response(serializer.data)

class SchoolAppCuratorsListView(generics.ListAPIView):
    permission_classes = [IsSchoolAdmin]
### dummy serializer not used
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

        return SchoolAppCurator.objects.all().filter(flow=flow_num)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = SchoolCuratorListSerializer(queryset, many=True)
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

            forms = SchoolAppForm.objects.filter(userinfo=request.user.ninfo)
            all_discounts = c_flow.discounts_by_orders.all()
            max_discount = 0
            founded_form = False
            for form in forms:
                if form.payed_amount != form.price:
                    continue
                for t in all_discounts:
                    if t.flow == form.flow:
                        founded_form = True
                        if t.discount > max_discount:
                            max_discount = t.discount


            if c_flow.avail_by_code and not founded_form:
                if code is not None and code.count() <= 0:
                    raise PermissionDenied({"message":
                                     "Код для записи на курс не корректен" })



            objs = SchoolAppForm.objects.filter(flow=c_flow,userinfo__id=request.user.ninfo.id)
            if objs.count() > 0:
                objs = objs.first()
                print('userinfo available')
            else:
                objs = ser.save()
                objs.userinfo = request.user.ninfo
                objs.save()
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

                if max_discount > 0:
                    objs.price = objs.price - max_discount
                    objs.save()

            ser = SchoolAppFormCreateSerializer(objs)
            return Response(ser.data)

class SchoolAppCuratorCreateView(generics.CreateAPIView):
    serializer_class = SchoolAppCuratorCreateSerializer
    queryset = SchoolAppCurator.objects.all()
    permission_classes = [IsAuthenticated]

    def post(cls, request, format=None):
        ser = SchoolAppCuratorCreateSerializer(data=request.data)
        if (ser.is_valid(raise_exception=True)):
            cc_flow = request.data.get('flow')
            if cc_flow is None:
                cc_flow=5
            c_flow = get_object_or_404(SchoolAppFlow,id=cc_flow)
            if c_flow.state == 0 or c_flow.state == 4:
                raise PermissionDenied({"message":"Запись на этот поток/курс не активна" })
            objs = SchoolAppCurator.objects.filter(flow=c_flow,userinfo=request.user.ninfo)
            if objs.count() > 0:
                objs = objs.first()
                ser = SchoolAppCuratorCreateSerializer(objs)
            else:
                objs = ser.save()
                objs.userinfo = request.user.ninfo
                objs.save()
            
            return Response(ser.data)


class SchoolAppFlowListView(generics.ListCreateAPIView):
    permission_classes = [IsSchoolAdmin]
    serializer_class = SchoolAppFlowListSerializer

    def list(self, request):
        queryset = SchoolAppFlow.objects.all()
        serializer = SchoolAppFlowListSerializer(queryset, many=True)
        return Response(serializer.data)

class SchoolAppFlowView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSchoolAdmin]
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
    lookup_field = 'slug__iexact'
    permission_classes = [AllowAny]


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
        if obj.userinfo != request.user.ninfo:
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
            if k.is_paid():
                total += k.amount

        if request.data['amount'] > inst.price*100-total:
            return Response({"amount" : "Введенная сумма слишком велика"},status=status.HTTP_400_BAD_REQUEST)

        inst.create_payment(amount=request.data['amount'])
        inst.save()

        return super(SchoolAppFormShowUpdateURLView,self).put(request,*args,**kwargs)


    def patch(self, request, *args, **kwargs):
        inst = self.get_object()

        for k in inst.payment.all():
            if not k.is_paid():
                if k.status == 'NEW' or k.status == 'FORM_SHOWED' or k.status == 'AUTH_FAIL' and k.error_code == 0:
                    inst.cancel_payment(k)

        return super(SchoolAppFormShowUpdateURLView,self).put(request,*args,**kwargs)
        

class SchoolAppFormCreateCreditPayURLView(View):

    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        id = self.kwargs.get('id', None)
        
        if id is None:
            return HttpResponseBadRequest()


        form = get_object_or_404(SchoolAppForm,pk=id)

        if request.user.ninfo != form.userinfo:
            return HttpResponseForbidden()

        if not hasattr(form,'credit'):
            cr_app = CreditApplication()
            cr_app.schoolappform = form
            cr_app.order_obj = str(form.id)
            cr_app.order_type ='Обучение в школе'
            cr_app.settings=TinkoffCreditSettings.objects.first()
            cr_app.first_name = request.user.ninfo.first_name
            cr_app.last_name = request.user.ninfo.last_name
            cr_app.middle_name = request.user.ninfo.middle_name
            cr_app.phone = request.user.ninfo.phone
            cr_app.email = request.user.ninfo.email
            cr_app.save()
        
            cr_arr = CreditApplicationItemsArray()
            cr_arr.application = cr_app
            cr_arr.save()
        
            cr_item = CreditApplicationItemsItem()
            cr_item.quantity = 1
            cr_item.name = 'Обучение в школе неНумерологии Ольги Перцевой'
            cr_item.price = form.price - form.payed_amount
            cr_item.array = cr_arr
            cr_item.save()
            
            tch = TinkoffCreditAPI()
            tch.create(cr_app)
        data = {
            'tcb_url': form.credit.link_url
        }
        return JsonResponse(data)
        

class SchoolPersCuratorPayView(generics.CreateAPIView):

    serializer_class = SchoolPersCuratorSerializer
    permission_classes = [IsAuthenticated]

class SchoolApplyPersCurator(View):
    def get(self, request, *args, **kwargs):
    
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        id = self.kwargs.get('id', None)

        if id is None:
            return HttpResponseForbidden()

        obj = get_object_or_404(SchoolAppPersCuratorForm,id=id)

        if obj.userinfo != request.user.ninfo:
            return HttpResponseForbidden()

        ser = SchoolPersCuratorSerializer(obj)
        return JsonResponse(ser.data)

    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        json_data = json.loads(request.body.decode('utf-8'))
        flow = get_object_or_404(SchoolAppFlow,id=json_data['flow_id'])
        form = get_object_or_404(SchoolAppForm,id=json_data['form_id'])
        if flow != form.flow:
            return HttpResponseForbidden()

        qs = SchoolAppPersCuratorForm.objects.filter(flow=flow,userinfo=request.user.ninfo)
        if qs.first() is not None:
            return JsonResponse(SchoolPersCuratorSerializer(qs.first()).data)

        cur = SchoolAppPersCuratorForm()

        cur.flow = flow
        cur.price = flow.pers_cur_price
        cur.userinfo = request.user.ninfo
        test_c = True
        for term in json_data['accepted_toss']:
            tobj = get_object_or_404(TermsOfServicePage,id=term)
            if tobj not in flow.pers_cur_toss.all():
                test_c = False

        if not test_c:
            return HttpResponseBadRequest

### for add many to many - we first need to save and get object
        cur.save()


        for term in json_data['accepted_toss']:
            tobj = get_object_or_404(TermsOfServicePage,id=term)
            cur.accepted_toss.add(tobj)

        cur.save()

### here we must return AppCuratorObject

        ser = SchoolPersCuratorSerializer(cur)
        return JsonResponse(ser.data)


class SchoolApplyPersCuratorGetPayURL(View):
    def put(self, request, *args, **kwargs):


        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        id = self.kwargs.get('id', None)
        
        if id is None:
            return HttpResponseBadRequest()


        pform = get_object_or_404(SchoolAppPersCuratorForm,pk=id)

        if request.user.ninfo != pform.userinfo:
            return HttpResponseForbidden()

        json_data = json.loads(request.body.decode('utf-8'))


        if json_data['amount']  <= 0:
            return Response({"amount" : "Интересная попытка :)"},status=status.HTTP_400_BAD_REQUEST)
#        if request.data['amount'] % 100000 != 0:
#            return Response({"amount" : "Некорректное значение"},status=status.HTTP_400_BAD_REQUEST)
        if json_data['amount'] > pform.price*100:
            return Response({"amount" : "Введенная сумма слишком велика"},status=status.HTTP_400_BAD_REQUEST)


        total = 0
        for k in pform.payment.all():
            if k.is_paid():
                total += k.amount

        if json_data['amount'] > pform.price*100-total:
            return Response({"amount" : "Введенная сумма слишком велика"},status=status.HTTP_400_BAD_REQUEST)


        pform.create_payment(amount=json_data['amount'])

        ser = SchoolPersCuratorSerializer(pform)
        return JsonResponse(ser.data)

class SchoolAppFromFilterByPayDate(View):
    def get(self, request, *args, **kwargs):


        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        if not request.user.is_superuser:
            return HttpResponseForbidden()


        date = self.kwargs.get('date', None)
        dtime = datetime.strptime("24-8-2019 15:00:00","%d-%m-%Y %H:%M:%S")
        dt = datetime.strptime("24-8-2017 15:00:00","%d-%m-%Y %H:%M:%S").replace(tzinfo=timezone.utc)
        objs = SchoolAppForm.get_registered_from_date(dt)
        print(objs)



class FileSchoolServeView(PrivateStorageDetailView):
    model=SchoolScanFile
    model_file_field='file'

    def can_access_file(self, private_file):
        obj = self.object
        if obj.order.userinfo.user.id == self.request.user.id:
            return True
        return False


class SchoolAppFormUpdateFileUploadView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SchoolAppFormSerializer

    def get_object(self):
        id = self.kwargs.get('id', None)
        user = self.request.user
        qs = SchoolAppForm.objects.filter(pk=id).first()
        if not qs is None:
            if qs.userinfo.user == user:
                return qs
            else:
                return None
        return qs

    def put(self, request, *args, **kwargs):
        inst = self.get_object()
        if inst is None:
            return HttpResponseForbidden()

        for f in request.FILES.getlist('file'):
            app = SchoolScanFile()
            app.title=f.name
            app.order = inst
            app.file = f
            app.save()

        return super(SchoolAppFormUpdateFileUploadView,self).get(request,*args,**kwargs)


class SchoolAppDiscountsListAPView(generics.ListCreateAPIView):
    permission_classes = [IsSchoolAdmin]
    serializer_class = SchoolAppDiscountCreateSerializer

    queryset = SchoolDiscount.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = SchoolAppDiscountListSerializer(queryset, many=True)
        return Response(serializer.data)



class SchoolExtendCreateView(generics.CreateAPIView):
    serializer_class = SchoolExtendAccessServiceCreateSerializer
    queryset = SchoolExtendAccessService.objects.all()
    permission_classes = [IsAuthenticated]

    def post(cls, request, format=None):
        ser = SchoolExtendAccessServiceCreateSerializer(data=request.data)
        if (ser.is_valid(raise_exception=True)):

            cc_flow = request.data.get('form')

            c_flow = get_object_or_404(SchoolAppForm,id=cc_flow)
            if c_flow.userinfo.id != request.user.ninfo.id:
                raise PermissionDenied({"message":"Нет доступа" })

            objs = ser.save()
            objs.price = objs.form.flow.extend_price
            objs.userinfo = request.user.ninfo
            objs.save()

            ret_ser = SchoolExtendAccessServiceSerializer(objs)
            return JsonResponse(ret_ser.data)


class SchoolExtendShowUpdateURL(generics.UpdateAPIView):

    serializer_class = SchoolExtendAccessServiceSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        id = self.kwargs.get('id', None)

        return get_object_or_404(SchoolExtendAccessService,pk=id)

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
            if k.is_paid():
                total += k.amount

        if request.data['amount'] > inst.price*100-total:
            return Response({"amount" : "Введенная сумма слишком велика"},status=status.HTTP_400_BAD_REQUEST)

        inst.create_payment(amount=request.data['amount'])
        inst.save()

        return super(SchoolExtendShowUpdateURL,self).put(request,*args,**kwargs)


    def patch(self, request, *args, **kwargs):
        inst = self.get_object()

        for k in inst.payment.all():
            if not k.is_paid():
                if k.status == 'NEW' or k.status == 'FORM_SHOWED' or k.status == 'AUTH_FAIL' and k.error_code == 0:
                    inst.cancel_payment(k)

        return super(SchoolExtendShowUpdateURL,self).put(request,*args,**kwargs)



class SchoolExtendShowUpdateView(generics.RetrieveAPIView):

    serializer_class = SchoolExtendAccessServiceSerializer
    permisiion_classes = [IsAuthenticated]

    def get_object(self):

        id = self.kwargs.get('id', None)

        return get_object_or_404(SchoolExtendAccessService,pk=id)


    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.form.userinfo != request.user.ninfo:
             raise PermissionDenied({"message":"У вас нет прав доступа для просмотра данных" })

        return super(SchoolExtendShowUpdateView,self).get(request,*args,**kwargs)


class SchoolSaleUpdateURL(generics.UpdateAPIView):

    serializer_class = SchoolAppFormSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        id = self.kwargs.get('id', None)

        return get_object_or_404(SchoolAppForm,pk=id)




    def put(self, request, *args, **kwargs):
        inst = self.get_object()


        if request.data['saleCode'] == '':
            return Response({"saleCode" : "Интересная попытка :)"},status=status.HTTP_400_BAD_REQUEST)

        cccode= request.data['saleCode']

        cc_code = PromoCode.objects.filter(code=cccode,flow=inst.flow)

        if cc_code is None:
            return Response({"saleCode" : "Код неактивен"},status=status.HTTP_400_BAD_REQUEST)

        cc_code = cc_code.first()

        if cc_code is None:
            return Response({"saleCode" : "Код неактивен"},status=status.HTTP_400_BAD_REQUEST)




        res = inst.apply_promocode(cc_code)

        if not res:
            return Response({"saleCode" : "Код неактивен"},status=status.HTTP_400_BAD_REQUEST)


        return super(SchoolSaleUpdateURL,self).put(request,*args,**kwargs)

class SchoolExtendTestView(View):

    def get(self, request, *args, **kwargs):
        user_email  = request.GET.get('email',None)
        user_phone  = request.GET.get('phone',None)
        end_time = request.GET.get('endtime',None)
        link = request.GET.get('link',None)
        flow = SchoolAppFlow.objects.filter(getcourse_url=link)
        if not flow:
            return HttpResponseForbidden()
        flow = flow.first()
        locale.setlocale(locale.LC_ALL, 'ru_RU')
        datetime_object = datetime.strptime(end_time, '%d %b %Y').date()
        userinfo = UserInfo.objects.filter(phone=user_phone, email=user_email)
        sc_ext = None
        if userinfo:
            sc_ext = SchoolAppForm.objects.filter(userinfo=userinfo.first(),flow=flow)
        if not sc_ext:
            return HttpResponseForbidden()
        sc = sc_ext.first()
        if sc.access_till is None:
            return HttpResponseBadRequest()
        diff_date = sc.access_till - datetime_object
        print(diff_date)
        print(diff_date.days)
        if diff_date.days > 0:
            return JsonResponse(True,safe=False)
        else:
            return JsonResponse(False, safe=False)



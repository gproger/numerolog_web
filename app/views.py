from django.http import Http404
from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect

from django.db.models import Q
from .models import AppOrder, AppResultFile, AppExpertUser

from .serializers import AppOrderSerializer, AppWorkSerializer
from .serializers import AppOrderItemExtSerializer
from .serializers import AppOrderCreateSerializer
from .serializers import AppExpertCheckSerializer
from .serializers import AppManagerOrderSerializer
from .serializers import AppOrderChangeGetSerializer
from .serializers import AppOrderChangeUpdateSerializer
from private_storage.views import PrivateStorageDetailView
import pprint
import datetime
from promocode.models import PromoCode
from schoolform.models import PriceField


class AppOrderListViewSet(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AppOrderSerializer

    def list(self, request):
        email = request.data.get('email').strip().lower()
        phone = request.data.get('phone').strip().lower()


class AppOrderCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AppOrderCreateSerializer
    queryset = AppOrder.objects.all()

class AppWorkListViewSet(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AppOrderSerializer

    def list(self, request):
        queryset = AppOrder.objects.filter(doer=request.user)
        serializer = AppWorkSerializer(queryset, many=True)
        return Response(serializer.data)


class AppOrderManagerListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AppOrderSerializer

    def list(self, request):
        queryset = AppOrder.objects.filter(items__auto__isnull=True)
        serializer = AppManagerOrderSerializer(queryset, many=True)
        return Response(serializer.data)




class AppOrderItemView(generics.RetrieveUpdateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = AppOrderItemExtSerializer

    def get_object(self):
        id = self.kwargs.get('id', None)
        user = self.request.user
        qs = AppOrder.objects.filter(Q(doer=user)|Q(owner=user)).filter(pk=id).first()
        return qs

    def put(self, request, *args, **kwargs):
        inst = self.get_object()
        code = request.data.get('code',None)
        if code:
            print(code)
            c_model = PromoCode.objects.filter(code=code,services=True,elapsed_count__gte=1)
            if not c_model:
                return HttpResponseBadRequest()

            if inst.price_f:
                return HttpResponseBadRequest()

            pr_field = PriceField()
            pr_field.price = inst.price
            c_model = c_model.first()

            if not c_model:
                return HttpResponseBadRequest()

            if c_model.is_percent:
                pr_field.discount = pr_field.price*c_model.discount/100
            else:
                pr_field.discount = c_model.discount

            inst.price = pr_field.price - pr_field.discount
            pr_field.save()
            inst.price_f = pr_field
            inst.save()
            c_model.price.add(pr_field)
            c_model.elapsed_count = c_model.elapsed_count - 1
            c_model.save()
            return super(AppOrderItemView,self).put(request,*args,**kwargs)
        else:
            print("code not available")
        return HttpResponseForbidden()

    def patch(self, request, *args, **kwargs):

        return HttpResponseForbidden

class AppOrderItemShowUpdateConfirmView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AppOrderItemExtSerializer

    def get_object(self):
        id = self.kwargs.get('id', None)
        user = self.request.user
        qs = AppOrder.objects.filter(Q(doer=user)).filter(pk=id).first()
        return qs

    def patch(self, request, *args, **kwargs):
        inst = self.get_object()
        exp_id = request.user.expert_rec.id
        for item in inst.workstate['assign']:
            if item['exp_id'] == exp_id and item['pending']== True and item['confirmed']==False:
                item['pending']=False
                item['confirmed']=True
                item['tstamp']=datetime.datetime.now().isoformat()
                dd_line = request.data.get("dd")
                dd_line = dd_line.split('.')
                cc_line = request.data.get("cc")
                cc_line = cc_line.split('.')
                inst.deadline_at=datetime.datetime(int(dd_line[2]),int(dd_line[1]),int(dd_line[0]),18,0,0)
                inst.consult_at=datetime.datetime(int(cc_line[2]),int(cc_line[1]),int(cc_line[0]),18,0,0)
        inst.save()

        return super(AppOrderItemShowUpdateConfirmView,self).put(request,*args,**kwargs)

    def put(self, request, *args, **kwargs):
        inst = self.get_object()
        exp_id = request.user.expert_rec.id
        for item in inst.workstate['assign']:
            if item['exp_id'] == exp_id and item['pending']== True and item['confirmed']==False:
                item['pending']=False
                item['confirmed']=False
                item['tstamp']=datetime.datetime.now().isoformat()
                item['comment']=request.data.get("comment")
        inst.doer = None
        inst.save()
        inst.change_expert()

        return super(AppOrderItemShowUpdateConfirmView,self).put(request,*args,**kwargs)

class AppOrderItemShowUpdateFileUploadView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AppOrderItemExtSerializer

    def get_object(self):
        id = self.kwargs.get('id', None)
        user = self.request.user
        qs = AppOrder.objects.filter(Q(doer=user)).filter(pk=id).first()
        return qs

    def put(self, request, *args, **kwargs):
        inst = self.get_object()
        exp_id = request.user.expert_rec.id
        for f in request.FILES.getlist('file'):
            app = AppResultFile()
            app.title=f.name
            app.order = inst
            app.file = f
            app.save()

        return super(AppOrderItemShowUpdateFileUploadView,self).get(request,*args,**kwargs)

class AppOrderItemShowUpdateURLView(generics.RetrieveUpdateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = AppOrderItemExtSerializer

    def get_object(self):
        id = self.kwargs.get('id', None)
        user = self.request.user
        qs = AppOrder.objects.filter(Q(doer=user)|Q(owner=user)).filter(pk=id).first()
        return qs

    def put(self, request, *args, **kwargs):
        inst = self.get_object()
        if inst is None:
            return Response({"amount" : "Услуга не найдена"},status=status.HTTP_404_BAD_REQUEST)
      
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

        return super(AppOrderItemShowUpdateURLView,self).put(request,*args,**kwargs)


    def patch(self, request, *args, **kwargs):
        inst = self.get_object()

        if inst is None:
            return Response({"amount" : "Услуга не найдена"},status=status.HTTP_404_BAD_REQUEST)
        
        for k in inst.payment.all():
            if not k.is_paid():
                if k.status == 'NEW' or k.status == 'FORM_SHOWED' or k.status == 'AUTH_FAIL' and k.error_code == 0:
                    inst.cancel_payment(k)

        return super(AppOrderItemShowUpdateURLView,self).get(request,*args,**kwargs)


class AppCheckExpertView(generics.ListAPIView):
    permission_classes=[AllowAny]
    serializer_class = AppExpertCheckSerializer

    def get_queryset(self):
        query_params = self.request.query_params
        first_name = query_params.get('first_name',None)
        last_name = query_params.get('last_name',None)
        middle_name = query_params.get('middle_name',None)
        code = query_params.get('code',None)

        ### check for mandatory params - by good practice we need return http request with 400 status

        qs = AppExpertUser.objects.all()
        if first_name is not None:
            qs.filter(first_name__iexact=first_name)
        
        if last_name is not None:
            qs.filter(last_name__iexact=last_name)
        
        if code is not None:
            qs.filter(code__iexact=code)
        
        if middle_name is not None:
            qs.filter(middle_name__iexact=middle_name)

        return qs



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





class AppOrderManagerItemView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AppOrderChangeGetSerializer

    def get_object(self):
        id = self.kwargs.get('id', None)
        qs = AppOrder.objects.get(pk=id)
        return qs


    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AppOrderChangeGetSerializer
        else:
            return AppOrderChangeUpdateSerializer


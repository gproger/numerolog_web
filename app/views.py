from django.http import Http404
from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied

from django.db.models import Q
from .models import AppOrder, AppResultFile

from .serializers import AppOrderSerializer, AppWorkSerializer
from .serializers import AppOrderItemExtSerializer
from .serializers import AppOrderCreateSerializer
from private_storage.views import PrivateStorageDetailView



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


class AppOrderItemView(generics.RetrieveUpdateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = AppOrderItemExtSerializer

    def get_object(self):
        id = self.kwargs.get('id', None)
        user = self.request.user
        qs = AppOrder.objects.filter(Q(doer=user)|Q(owner=user)).filter(pk=id).first()
        return qs


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

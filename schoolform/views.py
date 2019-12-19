from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model

from .models import SchoolAppForm, SchoolAppFlow, SchoolAppCurator

from .serializers import SchoolAppFormSerializer, SchoolAppFlowListSerializer
from .serializers import SchoolAppFormCreateSerializer,SchoolAppFormFlowStudentsList
from .serializers import SchoolAppFlowSerializer, SchoolAppFlowWOChoicesSerializer, SchoolAppCuratorCreateSerializer
from .serializers import SchoolPersCuratorSerializer
from django.shortcuts import render, get_object_or_404

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
    permission_classes = [AllowAny]

    def post(cls, request, format=None):
        ser = SchoolAppFormCreateSerializer(data=request.data)
        print(request.data)
        if (ser.is_valid(raise_exception=True)):
            cc_flow = request.data.get('flow_id')
            c_flow = get_object_or_404(SchoolAppFlow,id=cc_flow)
            if c_flow.state != 1:
                raise PermissionDenied({"message":"Запись на этот поток/курс не активна" })
                 
            objs = SchoolAppForm.objects.filter(flow=c_flow,email=request.data.get('email').strip().lower())
            if objs.count() > 0:
                objs = objs.first()
                ser = SchoolAppFormCreateSerializer(objs)
            else:
                objs = ser.save()
            return Response(ser.data)

class SchoolAppCuratorCreateView(generics.CreateAPIView):
    serializer_class = SchoolAppCuratorCreateSerializer
    queryset = SchoolAppCurator.objects.all()
    permission_classes = [AllowAny]

    def post(cls, request, format=None):
        ser = SchoolAppCuratorCreateSerializer(data=request.data)
        print(request.data)
        if (ser.is_valid(raise_exception=True)):
            cc_flow = request.data.get('flow_id')
            c_flow = get_object_or_404(SchoolAppFlow,id=cc_flow)
            if c_flow.state != 1:
                raise PermissionDenied({"message":"Запись на этот поток/курс не активна" })
            objs = SchoolAppCurator.objects.filter(flow=c_flow,email=request.data.get('email').strip().lower())
            if objs.count() > 0:
                objs = objs.first()
                ser = SchoolAppCuratorCreateSerializer(objs)
            else:
                objs = ser.save()
            return Response(ser.data)


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
            obj = SchoolAppFlow.objects.get(pk=id)
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

        if id is None:
            return SchoolAppForm.objects.none()
        try:
            obj = SchoolAppForm.objects.get(pk=id)
        except SchoolAppForm.DoesNotExist:
            obj = None

        obj.get_payment_status()

        return obj

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
    permission_classes = [AllowAny]

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

#        obj.create_payment()

        return obj

    def put(self, request, *args, **kwargs):
        inst = self.get_object()
        
        if request.data['amount']  <= 0:
            return Response({"amount" : "Интересная попытка :)"},status=status.HTTP_400_BAD_REQUEST)
        if request.data['amount'] % 100000 != 0:
            return Response({"amount" : "Некорректное значение"},status=status.HTTP_400_BAD_REQUEST)
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

        print(request.data)
        return super(SchoolAppFormShowUpdateURLView,self).put(request,*args,**kwargs)

class SchoolPersCuratorPayView(generics.CreateAPIView):

    serializer_class = SchoolPersCuratorSerializer
    permission_classes = [AllowAny]

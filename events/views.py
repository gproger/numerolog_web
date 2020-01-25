from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404

from .models import OfflineEvent, EventTicketTemplate, Ticket
from promocode.models import PromoCode
from schoolform.models import PriceField

from .serializers import OfflineEventSerializer
from .serializers import EventTicketTemplateSerializer
from .serializers import TicketListSerializer
from .serializers import TicketCreateSerializer
from .serializers import EventTicketSaleSerializer
from .serializers import TicketAppFormSerializer
# Create your views here.


class OfflineActiveEventView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = EventTicketSaleSerializer

    def get_object(self):
        return EventTicketTemplate.objects.all().last()


class OfflineEventListView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = OfflineEventSerializer

    def list(self, request):
        queryset = OfflineEvent.objects.all()
        serializer = OfflineEventSerializer(queryset, many=True)
        return Response(serializer.data)

class OfflineEventRUDView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = OfflineEventSerializer

    def get_object(self):
        id = self.kwargs.get('id', None)

        return get_object_or_404(OfflineEvent,pk=id)


class EventTicketTemplateListView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = EventTicketTemplateSerializer

    def list(self, request):
        ev_id = self.kwargs.get('event', None)
        queryset = EventTicketTemplate.objects.filter(event__id=ev_id)
        serializer = EventTicketTemplateSerializer(queryset, many=True)
        return Response(serializer.data)

class EventTicketTemplateRUDView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = EventTicketTemplateSerializer

    def get_object(self):
        id = self.kwargs.get('id', None)

        return get_object_or_404(EventTicketTemplate,pk=id)

class TicketListView(generics.ListAPIView):

    permission_classes = [IsAdminUser]
    serializer_class = TicketListSerializer

    def get_queryset(self):
        query_params = self.request.query_params
        event_num = self.kwargs.get('event', None)
        if event_num == None:
                return None
        else:
            try:
                event_num = OfflineEvent.objects.get(id=event_num)
            except OfflineEvent.DoesNotExist:
                return None

        return Ticket.objects.all().filter(eventticket__event=event_num)

    def list(self, request, event):
        queryset = self.get_queryset()
        serializer = TicketListSerializer(queryset, many=True)
        return Response(serializer.data)

class TicketAddView(generics.CreateAPIView):
    serializer_class = TicketCreateSerializer
    queryset = Ticket.objects.all()
    permission_classes = [AllowAny]

    def post(cls, request, format=None):
        ser = TicketCreateSerializer(data=request.data)
        print(request.data)
        if (ser.is_valid(raise_exception=True)):
            cc_event = request.data.get('eventticket')
            cc_event = get_object_or_404(EventTicketTemplate,id=cc_event)
            cc_code = request.data.get('code', None)

            if cc_event.get_time_delta_start() < 0:
                raise PermissionDenied({"message":"Продажи билетов ещё не начались" })

            if cc_event.get_time_delta_start() < 0:
                raise PermissionDenied({"message":"Продажи билетов окончены" })

            if cc_event.elapsed_count() < request.data.get('count'):
                raise PermissionDenied({"message":"Заказанное количество билетов не доступно" })


            code = None

            if cc_code is not None:
                code = PromoCode.objects.filter(evticket=cc_event,
                                                code=cc_code,
                                                elapsed_count__gte=1)


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


class TicketShowUpdateView(generics.RetrieveAPIView):

    serializer_class = TicketAppFormSerializer
    permisiion_classes = [AllowAny]

    def get_object(self):

        id = self.kwargs.get('id', None)

        return get_object_or_404(Ticket,pk=id)

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        email = request.GET.get('email', None)
        if email is None:
             raise PermissionDenied({"message":"У вас нет прав доступа для просмотра данных" })
        if email.lower() != obj.email.lower():
             raise PermissionDenied({"message":"У вас нет прав доступа для просмотра данных" })

        return super(TicketShowUpdateView,self).get(request,*args,**kwargs)


class TicketShowUpdateURLView(generics.UpdateAPIView):

    serializer_class = TicketAppFormSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        id = self.kwargs.get('id', None)

        return get_object_or_404(Ticket,pk=id)

    def put(self, request, *args, **kwargs):
        inst = self.get_object()

        if request.data['amount']  <= 0:
            return Response({"amount" : "Интересная попытка :)"},status=status.HTTP_400_BAD_REQUEST)
        if request.data['amount'] % 10000 != 0:
            return Response({"amount" : "Некорректное значение"},status=status.HTTP_400_BAD_REQUEST)
        if request.data['amount'] > inst.price*100:
            return Response({"amount" : "Введенная сумма слишком велика"},status=status.HTTP_400_BAD_REQUEST)
        if request.data['amount'] != inst.price*100:
            return Response({"amount" : "Некорректное значение, необходимо оплатить всю сумму разом"},status=status.HTTP_400_BAD_REQUEST)


        total = 0
        for k in inst.payment.all():
            if k.status == 'CONFIRMED':
                total += k.amount

        if request.data['amount'] > inst.price*100-total:
            return Response({"amount" : "Введенная сумма слишком велика"},status=status.HTTP_400_BAD_REQUEST)

        inst.create_payment(amount=request.data['amount'])
        inst.save()

        print(request.data)
        return super(TicketShowUpdateURLView,self).put(request,*args,**kwargs)

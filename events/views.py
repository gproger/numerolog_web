from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model

from .models import OfflineEvent, EventTicketTemplate, Ticket

from .serializers import OfflineEventSerializer
from .serializers import EventTicketTemplateSerializer
from .serializers import TicketListSerializer
from .serializers import TicketCreateSerializer
# Create your views here.


class OfflineActiveEventView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = OfflineEventSerializer

    def get_object(self):
        return OfflineEvent.objects.all().last()


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
        obj = None
        if id is None:
            return OfflineEvent.objects.none()
        try:
            obj = OfflineEvent.objects.get(pk=id)
        except OfflineEvent.DoesNotExist:
            obj = None

        return obj

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
        obj = None
        if id is None:
            return EventTicketTemplate.objects.none()
        try:
            obj = EventTicketTemplate.objects.get(pk=id)
        except EventTicketTemplate.DoesNotExist:
            obj = None

        return obj


class TicketListView(generics.ListAPIView):

    permission_classes = [IsAdminUser]
    serializer_class = TicketListSerializer

    def get_queryset(self):
        query_params = self.request.query_params
        event_num = query_params.get('event', None)
        if event_num == None:
                return None
        else:
            try:
                event_num = OfflineEvent.objects.get(id=event_num)
            except OfflineEvent.DoesNotExist:
                return None

        return Ticket.objects.all().filter(eventticket__event=event_num)

    def list(self, request):
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
            cc_event = request.data.get('evtick_id')
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
                code = PromoCode.objects.filter(flow=c_flow,
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

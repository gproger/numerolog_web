from rest_framework import serializers

from django_tinkoff_merchant.serializers import PaymentSerializer
from .models import OfflineEvent, EventTicketTemplate, Ticket


class OfflineEventSerializer(serializers.ModelSerializer):

    created = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'],required=False)
    ticket_sale_start = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'],required=False)
    ticket_sale_stop = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'],required=False)
    description = serializers.CharField(required=False)
    address_url = serializers.URLField(required=False)
    toss = serializers.SerializerMethodField()
    cur_toss = serializers.SerializerMethodField()

    def get_cur_toss(self,obj):
        lis = []
        for x in obj.cur_toss.all():
            lis.append({'id': x.id,'title' : x.title})
        return lis

    def get_toss(self,obj):
        lis = []
        for x in obj.toss.all():
            lis.append({'id': x.id,'title' : x.title})
        return lis

    class Meta:
        model = OfflineEvent
        fields = '__all__'


class EventTicketTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventTicketTemplate
        fields = '__all__'


class TicketListSerializer(serializers.ModelSerializer):

    payment = PaymentSerializer(required=False, many = True)

    class Meta:
        model = Ticket
        fields = '__all__'

class TicketCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = '__all__'

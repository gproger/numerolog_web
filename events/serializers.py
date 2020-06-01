from rest_framework import serializers

from django_tinkoff_merchant.serializers import PaymentSerializer
from .models import OfflineEvent, EventTicketTemplate, Ticket


class OfflineEventSerializer(serializers.ModelSerializer):

    created = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'],required=False)
    ticket_sale_start = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'],required=False)
    ticket_sale_stop = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'],required=False)
    description = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    address_url = serializers.URLField(required=False)
    toss = serializers.SerializerMethodField()

    tickets = serializers.SerializerMethodField()
    tickets_sale = serializers.SerializerMethodField()

    def get_tickets(self, obj):
        evTicks = EventTicketTemplate.objects.filter(event=obj)
        res = 0
        for p in evTicks:
            res += p.ticket_cnt
        return res

    def get_tickets_sale(self, obj):
        evTicks = EventTicketTemplate.objects.filter(event=obj)
        res = 0
        for p in evTicks:
            res += p.solded_cnt
        return res


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
    amount = serializers.SerializerMethodField()
    promocode = serializers.SerializerMethodField()
    price_f = serializers.SerializerMethodField()

    def get_amount(self, obj):
        return obj.get_amount(obj)

    def get_promocode(self, obj):
        if hasattr( obj, 'price_f'):
            if obj.price_f is not None:
                return obj.price_f.promocode_set.all()[0].code
            else:
                return ''
        else:
            return ''

    def get_price_f(self, obj):
        if hasattr( obj, 'price_f'):
            if obj.price_f is not None:
                return obj.price_f.price
            else:
                return ''
        else:
            return ''

    class Meta:
        model = Ticket
        fields = '__all__'

class TicketCreateSerializer(serializers.ModelSerializer):

    def validate_phone(self, value):
        value = value.replace(" ","")
        value = value.replace("(","")
        value = value.replace(")","")
        value = value.replace("-","")
        return value

    class Meta:
        model = Ticket
        fields = '__all__'

class EventTicketSaleSerializer(serializers.ModelSerializer):

    toss = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()



    def get_toss(self,obj):
        lis = []
        for x in obj.event.toss.all():
            lis.append({'id': x.id,'title' : x.title})
        return lis

    def get_description(self,obj):
        return obj.event.description


    class Meta:
        model = EventTicketTemplate
        fields = ['toss','price','id','description']


class TicketAppFormSerializer(serializers.ModelSerializer):

    order = serializers.SerializerMethodField(required=False)

    payment = PaymentSerializer(required=False, many = True)

    amount = serializers.SerializerMethodField()

    phone_valid = serializers.BooleanField(required=False)

    def get_order(self,obj):
        order = []
        if not hasattr(obj,'id'):
            return order

        toss = []

        for x in obj.accepted_toss.all():
            toss.append({'url': '/tos/'+str(x.id),'title' : x.title})
        
        order.append({'name' : 'Билет №', 'value' : obj.id, 'type' : 'id'})
        order.append({'name' : 'Встреча:', 'value' : obj.eventticket.event.name, 'type' : 'event_name'})
        order.append({'name' : 'Фамилия:', 'value' : obj.last_name, 'type' : 'last_name'})
        order.append({'name' : 'Имя:', 'value' : obj.first_name, 'type' : 'first_name'})
        order.append({'name' : 'Отчество:', 'value' : obj.middle_name, 'type' : 'middle_name'})
        order.append({'name' : 'E-mail:', 'value' : obj.email, 'type' : 'email'})
        order.append({'name' : 'Телефон:', 'value' : obj.phone, 'type':'phone'})
        order.append({'name' : 'Стоимость участия:', 'value' : obj.price, 'type':'price'})
        order.append({'name' : 'Соглашения:', 'value' : toss, 'type' : 'toss'})
        #if hasattr(obj,'payed_outline'):
        #    if obj.payed_outline > 0:
        #        order.append({'name' : 'Предоплата:', 'value' : obj.payed_outline})



        #if hasattr(obj,'payed_by'):
        #    order.append({'name' : 'Оплачено на карту:', 'value' : obj.payed_outline})
        #if hasattr(obj,'payed_by'):
        #    if obj.payed_by != '':
        #        order.append({'name' : 'Оплачено от имени:', 'value' : obj.payed_by})

        return order

    def get_amount(self,obj):
        total = 0
        if not hasattr(obj,'payment'):
            return 0
        for k in obj.payment.all():
            if k.status == 'CONFIRMED':
                total += k.amount
        return total/100


    class Meta:
        model = Ticket
        fields = ['order','payment','amount','phone_valid']

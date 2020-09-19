
from rest_framework import serializers
from .models import AppOrder
from django_tinkoff_merchant.serializers import PaymentSerializer


class AppOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppOrder
        fields = '__all__'

class AppWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppOrder
        fields = '__all__'

class AppOrderItemExtSerializer(serializers.ModelSerializer):
    
    payment = PaymentSerializer(required=False, many=True)
    amount = serializers.SerializerMethodField()
    order = serializers.SerializerMethodField()

    def get_amount(self,obj):
        total = 0
        if not hasattr(obj,'payment'):
            return 0
        for k in obj.payment.all():
            if k.is_paid():
                total += k.amount
        if obj.payed_amount > total/100:
            total = obj.payed_amount*100
        return total/100

    def get_order(self,obj):
        order = []
        if not hasattr(obj,'id'):
            return order

        toss = []

        return []

        for x in obj.accepted_toss.all():
            toss.append({'url': '/tos/'+str(x.id),'title' : x.title})

        order.append({'name' : 'Заказ №', 'value' : obj.id, 'type' : 'id'})
        order.append({'name' : 'Поток обучения:', 'value' : obj.flow.flow, 'type' : 'flow_id'})
        order.append({'name' : 'Курс обучения:', 'value' : obj.flow.flow_name, 'type' : 'flow_name'})
        order.append({'name' : 'Фамилия:', 'value' : obj.last_name, 'type' : 'last_name'})
        order.append({'name' : 'Имя:', 'value' : obj.first_name, 'type' : 'first_name'})
        order.append({'name' : 'E-mail:', 'value' : obj.email, 'type' : 'email'})
        order.append({'name' : 'Телефон:', 'value' : obj.phone, 'type' : 'phone'})
        order.append({'name' : 'Стоимость услуги:', 'value' : obj.price, 'type' : 'price'})
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

    class Meta:
        model = AppOrder
        fields = ['payment','amount','order']

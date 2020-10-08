from django.urls import reverse
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
    cancelUrl = serializers.SerializerMethodField()
    confirmUrl = serializers.SerializerMethodField()
    uploadUrl = serializers.SerializerMethodField()

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

        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        toss = []


#        for x in obj.accepted_toss.all():
#            toss.append({'url': '/tos/'+str(x.id),'title' : x.title})

        order.append({'name' : 'Заказ №', 'value' : obj.id, 'type' : 'id'})
        if obj.owner.id == user.id:
            order.append({'name' : 'Исполнитель:', 'value' : obj.doer_name, 'type' : 'doer_name'})
        else:
            order.append({'name' : 'Заказчик:', 'value' : obj.first_name, 'type' : 'owner_name'})

        order.append({'name' : 'Создан:', 'value' : obj.created_at, 'type' : 'datetime'})
        order.append({'name' : 'Получение описания до:', 'value' : obj.deadline_at, 'type' : 'datetime'})
        order.append({'name' : 'Консультация:', 'value' : obj.consult_at, 'type' : 'datetime'})
        
        it_array = []
        for p in obj.items['items']:
            it_array.append({'name':'Имя:','value':p['name'],'type':'it_name'})
            it_array.append({'name':'Дата:','value':p['date'],'type':'date'})
            it_array.append({'name':'Пол:','value':p['gender'],'type':'gender'})


        order.append({'name':'Детали заказа:', 'value' : it_array, 'type': 'array'})

        order.append({'name' : 'Стоимость услуги:', 'value' : obj.price, 'type' : 'price'})

        files_array = []

        for p in obj.files.all():
            files_array.append({'name':p.title,'value':reverse('file_download',kwargs={'pk':p.id}),'type':'url'})

        if len(files_array) > 0:
            order.append({'name':'Файлы','value':files_array,'type':'array'})
        else:
            order.append({'name':'Файлы','value':'Файлов нет','type':'caption'})

        return order

    def get_cancelUrl(self, obj):
        return reverse('service_pay_view',kwargs={'id':obj.id})

    def get_confirmUrl(self, obj):
        founded = False
        if not hasattr(obj,'workstate'):
            return None
        if not 'assign' in obj.workstate:
            return None
        if not hasattr(self.context['request'].user,'expert_rec'):
            return None
        if self.context['request'].user.expert_rec is None:
            return None
        exp_id = self.context['request'].user.expert_rec.pk
        for item in obj.workstate['assign']:
            if item['exp_id'] == exp_id and item['pending']==True and item['confirmed']==False:
                founded = True

        if founded:
            return reverse('service_expert_confirm',kwargs={'id':obj.id})
        else:
            return None

    def get_uploadUrl(self, obj):
        founded = False
        if not hasattr(obj,'workstate'):
            return None
        if not 'assign' in obj.workstate:
            return None
        if not hasattr(self.context['request'].user,'expert_rec'):
            return None
        if self.context['request'].user.expert_rec is None:
            return None
        exp_id = self.context['request'].user.expert_rec.pk
        for item in obj.workstate['assign']:
            if item['exp_id'] == exp_id and item['pending']==False and item['confirmed']==True:
                founded = True

        if founded:
            return reverse('service_expert_upload',kwargs={'id':obj.id})
        else:
            return None


    class Meta:
        model = AppOrder
        fields = ['payment','amount','order','cancelUrl','confirmUrl','uploadUrl']


class AppOrderCreateSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'], required=False)
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    payment = PaymentSerializer(required=False, many=True, read_only=True)

    class Meta:
        model = AppOrder
        exclude = ['doer','name','workstate']

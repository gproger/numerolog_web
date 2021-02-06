from django.urls import reverse
from rest_framework import serializers
from .models import AppOrder
from .models import AppExpertUser
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
    saleUrl = serializers.SerializerMethodField()

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

        contact_array=[]
        if obj.owner.id == user.id:
            contact_array.append({'name' : 'Исполнителю', 'value' : 'https://wa.me/'+obj.doer_phone[1:], 'type' : 'url'})
            contact_array.append({'name' : 'В поддержку', 'value' : 'https://wa.me/79687432507', 'type' : 'url'})
        else:
            contact_array.append({'name' : 'Заказчику:', 'value' : 'https://wa.me/'+obj.owner_phone[1:], 'type' : 'url'})

        order.append({'name':'Написать сообщение:','value':contact_array,'type':'array'})

        order.append({'name' : 'Создан:', 'value' : obj.created_at, 'type' : 'datetime'})
        order.append({'name' : 'Получение описания до:', 'value' : obj.deadline_at, 'type' : 'datetime'})
        order.append({'name' : 'Консультация:', 'value' : obj.consult_at, 'type' : 'datetime'})
        
        it_array = []
        for p in obj.items['items']:
            it_array.append({'name':'Имя:','value':p['name'],'type':'it_name'})
            it_array.append({'name':'Дата:','value':p['date'],'type':'date'})
            it_array.append({'name':'Пол:','value':p['gender'],'type':'gender'})


        order.append({'name':'Детали заказа:', 'value' : it_array, 'type': 'array'})

        if obj.price_f:
            order.append({'name' : 'Промокод:', 'value' : obj.price_f.promocode_set.first().code, 'type' : 'caption'})
            order.append({'name' : 'Скидка:', 'value' : str(obj.price_f.discount) + ' Руб.', 'type' : 'caption'})

        order.append({'name' : 'Стоимость услуги:', 'value' : obj.price, 'type' : 'price'})



        files_array = []

        for p in obj.files.all():
            files_array.append({'name':p.title,'value':reverse('file_download',kwargs={'pk':p.id}),'type':'url'})

        if len(files_array) > 0:
            order.append({'name':'Файлы','value':files_array,'type':'array'})
        else:
            order.append({'name':'Файлы','value':'Файлов нет','type':'caption'})

        order.append({'name' : 'Комментарий к заказу:', 'value' : obj.comment, 'type' : 'comment'})

        if obj.owner.id != user.id:
            order.append({'name' : 'Личный комментарий(заметки):', 'value' : obj.expertcomment, 'type' : 'comment'})




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


    def get_saleUrl(self, obj):

        if obj.price_f is not None:
            return None

        if obj.payed_amount == obj.price:
            return None

        return reverse('serv_view_url',kwargs={'id':obj.id})

    class Meta:
        model = AppOrder
        fields = ['payment','amount','order','cancelUrl','confirmUrl','uploadUrl','saleUrl']


class AppOrderCreateSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'], required=False)
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    payment = PaymentSerializer(required=False, many=True, read_only=True)

    class Meta:
        model = AppOrder
        exclude = ['doer','name','workstate']


class AppExpertCheckSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppExpertUser
        fields = ['first_name','last_name','middle_name','phone','email','active','workstate','orders_in_work']


class AppManagerOrderSerializer(serializers.ModelSerializer):
    doer = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    payment = PaymentSerializer(required=False, many=True, read_only=True)
    created = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'], required=False)
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'], required=False)
    deadline_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'], required=False)
    consult_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'], required=False)

    def get_doer(self, obj):
        if obj.doer is None:
            return None

        res = {}
        res['first_name'] = obj.doer.ninfo.first_name
        res['last_name'] = obj.doer.ninfo.last_name
        res['middle_name'] = obj.doer.ninfo.middle_name
        res['email'] = obj.doer.ninfo.email
        res['phone'] = obj.doer.ninfo.phone
        return res


    def get_owner(self, obj):
        if obj.owner is None:
            return None

        res = {}
        res['first_name'] = obj.owner.ninfo.first_name
        res['last_name'] = obj.owner.ninfo.last_name
        res['middle_name'] = obj.owner.ninfo.middle_name
        res['email'] = obj.owner.ninfo.email
        res['phone'] = obj.owner.ninfo.phone
        return res


    class Meta:
        model = AppOrder
        fields = '__all__'



class AppOrderChangeUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppOrder
        fields = ['doer','comment']


class AppOrderChangeGetSerializer(serializers.ModelSerializer):

    doer = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    payment = PaymentSerializer(required=False, many=True, read_only=True)
    created = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'], required=False)
    deadline_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'], required=False)
    consult_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'], required=False)
    experts = serializers.SerializerMethodField()


    def get_doer(self, obj):
        if obj.doer is None:
            return None

        res = {}
        res['first_name'] = obj.doer.ninfo.first_name
        res['last_name'] = obj.doer.ninfo.last_name
        res['middle_name'] = obj.doer.ninfo.middle_name
        res['email'] = obj.doer.ninfo.email
        res['phone'] = obj.doer.ninfo.phone
        res['id']= obj.doer.id;
        return res


    def get_owner(self, obj):
        if obj.owner is None:
            return None

        res = {}
        res['first_name'] = obj.owner.ninfo.first_name
        res['last_name'] = obj.owner.ninfo.last_name
        res['middle_name'] = obj.owner.ninfo.middle_name
        res['email'] = obj.owner.ninfo.email
        res['phone'] = obj.owner.ninfo.phone
        return res

    def get_experts(self, obj):
        exp_ = AppExpertUser.objects.all()
        res = []
        for exp_i in exp_:
            res.append({'id':exp_i.user.pk,
                'first_name' : exp_i.user.ninfo.first_name,
                'last_name' : exp_i.user.ninfo.last_name,
                'middle_name' : exp_i.user.ninfo.middle_name,
                'email' : exp_i.user.ninfo.email,
                'phone' : exp_i.user.ninfo.phone,
                'active': exp_i.active
            })
        return res

    class Meta:
        model = AppOrder
        fields = ['owner','doer','created','consult_at','deadline_at','experts','payment','items','comment','expertcomment','admincomment']

from rest_framework import serializers
from .models import SchoolAppForm, SchoolAppFlow, SchoolAppCurator, SchoolAppPersCuratorForm
from django_tinkoff_merchant.serializers import PaymentSerializer

from users.serializers import UserInfoSerializer
from utils.phone import get_phone


class SchoolAppFormCreateSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'], required=False)

    def validate_email(self, value):
        norm_value = value.lower()
        return norm_value

    def validate_phone(self, value):
        get_phone(value)

    class Meta:
        model = SchoolAppForm
        exclude = ['payment']


class SchoolAppCuratorCreateSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'], required=False)
    flow = serializers.PrimaryKeyRelatedField(queryset=SchoolAppFlow.objects.all(),many=False)


    def validate_email(self, value):
        norm_value = value.lower()
        return norm_value


    class Meta:
        model = SchoolAppCurator
        fields = '__all__'

class SchoolAppFlowListSerializer(serializers.ModelSerializer):
    state = serializers.SerializerMethodField()
    created = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'],required=False)

    def get_state(self, obj):
        return obj.get_state_display()

    class Meta:
        model = SchoolAppFlow
        fields = ['state','created','flow','flow_name','id']


class SchoolAppFlowSerializer(serializers.ModelSerializer):
#    state = serializers.SerializerMethodField()
    state = serializers.ChoiceField(choices=SchoolAppFlow.STATES)
    created = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'], required=False)
    price = serializers.IntegerField(default=30000, required = False)

#   recruitment fields
    recruitment_start = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y'] , required = False)
    recruitment_stop = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y'] , required = False)

#   started fields
    education_start = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y'] , required = False)
    education_stop = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y'] , required = False)

    choices = serializers.SerializerMethodField()
    slug = serializers.SlugField( allow_unicode=True)

    def get_choices(self, obj):
        return SchoolAppFlow.STATES

    def get_state(self, obj):
        return obj.get_state_display()


    class Meta:
        model = SchoolAppFlow
        fields = '__all__'


class SchoolAppFlowWOChoicesSerializer(serializers.ModelSerializer):

#    state = serializers.SerializerMethodField()
    price = serializers.IntegerField(default=30000, required = False)

#   recruitment fields
    recruitment_start = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y'] , required = False)
    recruitment_stop = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y'] , required = False)

#   started fields
    education_start = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y'] , required = False)
    education_stop = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y'] , required = False)

    toss = serializers.SerializerMethodField()
    cur_toss = serializers.SerializerMethodField()
    pers_toss = serializers.SerializerMethodField()

    slug = serializers.SlugField(required = False)

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

    def get_pers_toss(self, obj):
        lis = []
        for x in obj.pers_cur_toss.all():
            lis.append({'id': x.id,'title' : x.title})
        return lis


    class Meta:
        model = SchoolAppFlow
        fields = '__all__'


class SchoolAppFlowWOChoicesSerializerBySlug(serializers.ModelSerializer):

#    state = serializers.SerializerMethodField()
    price = serializers.IntegerField(default=30000, required = False)

#   recruitment fields
    recruitment_start = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y'] , required = False)
    recruitment_stop = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y'] , required = False)

#   started fields
    education_start = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y'] , required = False)
    education_stop = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y'] , required = False)

    toss = serializers.SerializerMethodField()
    cur_toss = serializers.SerializerMethodField()
    pers_toss = serializers.SerializerMethodField()

    ninfo = serializers.SerializerMethodField()


    def get_ninfo(self, obj):
        uinfo = self.context.get('request').user.ninfo
        return UserInfoSerializer(uinfo).data

    

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

    def get_pers_toss(self, obj):
        lis = []
        for x in obj.pers_cur_toss.all():
            lis.append({'id': x.id,'title' : x.title})
        return lis


    class Meta:
        model = SchoolAppFlow
        lookup_field = 'slug'
        fields = '__all__'


class SchoolAppFormFlowStudentsList(serializers.ModelSerializer):

    amount = serializers.SerializerMethodField()
    created = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'], required=False)
    bid = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y'] , required = False)
    payment = PaymentSerializer(required=False, many = True)
    price_f = serializers.SerializerMethodField()
    promocode = serializers.SerializerMethodField()

    def get_price_f(self, obj):
        if hasattr( obj, 'price_f'):
            if obj.price_f is not None:
                return obj.price_f.price
            else:
                return obj.price
        else:
            return obj.price

    def get_promocode(self, obj):
        if hasattr( obj, 'price_f'):
            if obj.price_f is not None:
                return obj.price_f.promocode_set.all()[0].code
            else:
                return ''
        else:
            return ''


    def get_amount(self,obj):
        total = 0
        for k in obj.payment.all():
            if k.is_paid():
                total += k.amount
        return total/100

    class Meta:
        model = SchoolAppForm
        fields = ['first_name','middle_name','last_name','bid','phone','email','instagramm','created','payed_by','amount','payment','price','price_f','promocode','phone_valid','payed_amount']

class SchoolPersCuratorSerializer(serializers.ModelSerializer):

    payment = PaymentSerializer(required=False, many = True)
    amount = serializers.SerializerMethodField(required=False)
    order = serializers.SerializerMethodField(required=False)



    def get_order(self,obj):
        order = []
        if not hasattr(obj,'id'):
            return order
        order.append({'name' : 'Заказ №', 'value' : obj.id, 'type' : 'id'})
        order.append({'name' : 'Поток обучения:', 'value' : obj.flow.flow, 'type' : 'flow_id'})
        order.append({'name' : 'Курс обучения:', 'value' : obj.flow.flow_name, 'type' : 'flow_name'})
        order.append({'name' : 'Фамилия:', 'value' : obj.last_name, 'type' : 'last_name'})
        order.append({'name' : 'Имя:', 'value' : obj.first_name, 'type' : 'first_name'})
        order.append({'name' : 'E-mail:', 'value' : obj.email, 'type' : 'email'})
        order.append({'name' : 'Телефон:', 'value' : obj.phone, 'type' : 'phone'})
        order.append({'name' : 'Стоимость услуги:', 'value' : obj.price, 'type' : 'price'})
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
            if k.is_paid():
                total += k.amount
        if obj.payed_amount > total/100:
            total = obj.payed_amount*100
        return total/100


    class Meta:
        model = SchoolAppPersCuratorForm
        exclude = ['flow']


class SchoolAppFormSerializer(serializers.ModelSerializer):

    order = serializers.SerializerMethodField(required=False)

    payment = PaymentSerializer(required=False, many = True)

    amount = serializers.SerializerMethodField()

    cform = SchoolPersCuratorSerializer(required=False, many=False, read_only=True, source="get_curator_form")

    curator = serializers.SerializerMethodField(required=False)

    phone_valid = serializers.BooleanField(required=False)

    def get_order(self,obj):
        order = []
        if not hasattr(obj,'id'):
            return order
        order.append({'name' : 'Заказ №', 'value' : obj.id, 'type' : 'id'})
        order.append({'name' : 'Поток обучения:', 'value' : obj.flow.flow, 'type' : 'flow_id'})
        order.append({'name' : 'Курс обучения:', 'value' : obj.flow.flow_name, 'type' : 'flow_name'})
        order.append({'name' : 'Фамилия:', 'value' : obj.last_name, 'type' : 'last_name'})
        order.append({'name' : 'Имя:', 'value' : obj.first_name, 'type' : 'first_name'})
        order.append({'name' : 'E-mail:', 'value' : obj.email, 'type' : 'email'})
        order.append({'name' : 'Телефон:', 'value' : obj.phone, 'type' : 'phone'})
        order.append({'name' : 'Стоимость обучения:', 'value' : obj.price, 'type' : 'price'})
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
            if k.is_paid():
                total += k.amount
        if obj.payed_amount > total/100:
            total = obj.payed_amount*100
        return total/100

    def get_curator(self,obj):
        if obj.price != obj.payed_amount:
            return {}
        lis = []
        for x in obj.flow.pers_cur_toss.all():
            lis.append({'id': x.id,'title' : x.title})
        return {'price':obj.flow.pers_cur_price,'flow':obj.flow.id,'id':obj.id,'toss':lis}


    class Meta:
        model = SchoolAppForm
        fields = ['order','payment','amount','cform','curator','phone_valid']

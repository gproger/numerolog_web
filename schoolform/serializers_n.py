from rest_framework import serializers
from .models import SchoolAppForm, SchoolAppFlow
from django_tinkoff_merchant.serializers import PaymentSerializer

class SchoolAppFormCreateSerializer(serializers.ModelSerializer):
    bid = serializers.DateField(format="%d.%m.%Y",input_formats=['%d.%m.%Y'])
    created = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'], required=False)

    def validate_email(self, value):
        norm_value = value.lower()
        return norm_value

    class Meta:
        model = SchoolAppForm
        exclude = ['flow','payment']

class SchoolAppFormValidateEmailSerializer(serializers.ModelSerializer):
    
    def validate_email(self,value):
        norm_value = value.lower()
        return norm_value

    class Meta:
        model = SchollAppFormEmail
        exclude = ['code']


class SchoolAppFlowListSerializer(serializers.ModelSerializer):
    state = serializers.SerializerMethodField()
    created = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'],required=False)

    def get_state(self, obj):
        return obj.get_state_display()

    class Meta:
        model = SchoolAppFlow
        fields = ['state','created','flow']


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

    def get_toss(self,obj):
        lis = []
        for x in obj.toss.all():
            lis.append({'id': x.id,'title' : x.title})
        return lis

    class Meta:
        model = SchoolAppFlow
        fields = '__all__'

class SchoolAppFormFlowStudentsList(serializers.ModelSerializer):
    
    amount = serializers.SerializerMethodField()
    created = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'], required=False)
    bid = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y'] , required = False)


    def get_amount(self,obj):
        total = 0
        for k in obj.payment.all():
            if k.status == 'CONFIRMED':
                total += k.amount
        return total/100

    class Meta:
        model = SchoolAppForm
        fields = ['first_name','middle_name','last_name','bid','phone','email','instagramm','created','payed_by','amount']

class SchoolAppFormSerializer(serializers.ModelSerializer):

    order = serializers.SerializerMethodField(required=False)

    payment = PaymentSerializer(required=False, many = True)

    amount = serializers.SerializerMethodField()

    def get_order(self,obj):
        order = []
        if not hasattr(obj,'id'):
            return order
        order.append({'name' : 'Заказ №', 'value' : obj.id})
        order.append({'name' : 'Поток обучения:', 'value' : obj.flow.flow})
        order.append({'name' : 'Фамилия:', 'value' : obj.last_name})
        order.append({'name' : 'Имя:', 'value' : obj.first_name})
        order.append({'name' : 'E-mail:', 'value' : obj.email})
        order.append({'name' : 'Телефон:', 'value' : obj.phone})
        order.append({'name' : 'Стоимость обучения:', 'value' : obj.flow.price})
        if hasattr(obj,'payed_outline'):
            if obj.payed_outline > 0:
                order.append({'name' : 'Предоплата:', 'value' : obj.payed_outline})


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
        model = SchoolAppForm
        fields = ['order','payment','amount']


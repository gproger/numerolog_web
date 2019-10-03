from rest_framework import serializers
from .models import SchoolAppForm, SchoolAppFlow
from django_tinkoff_merchant.serializers import PaymentSerializer

class SchoolAppFormCreateSerializer(serializers.ModelSerializer):
    bid = serializers.DateField(format="%d.%m.%Y",input_formats=['%d.%m.%Y'])
    created = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'], required=False)

    class Meta:
        model = SchoolAppForm
        exclude = ['flow','payment']


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


class SchoolAppFormSerializer(serializers.ModelSerializer):

    order = serializers.SerializerMethodField()

    payment = PaymentSerializer()

    def get_order(self,obj):
        order = []
        order.append({'name' : 'Заказ №', 'value' : obj.id})
        order.append({'name' : 'Поток обучения:', 'value' : obj.flow.flow})
        order.append({'name' : 'Фамилия:', 'value' : obj.last_name})
        order.append({'name' : 'Имя:', 'value' : obj.first_name})
        order.append({'name' : 'E-mail:', 'value' : obj.email})
        order.append({'name' : 'Телефон:', 'value' : obj.phone})
        order.append({'name' : 'Стоимость обучения:', 'value' : obj.flow.price})

        return order

    class Meta:
        model = SchoolAppForm
        fields = ['order','payment']


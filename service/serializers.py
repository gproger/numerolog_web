from rest_framework import serializers
from .models import ServiceExpert, ServiceClient, ServiceToss

class ServiceExpertSerializer(serializers.ModelSerializer):

    slug = serializers.SlugField(required=False)
    balance = serializers.IntegerField(required=False)
    percent = serializers.IntegerField(required=True)

    def validate_email(self, value):
        norm_value = value.lower()
        return norm_value

    class Meta:
        model = ServiceExpert
        fields = '__all__'

class ServiceClientSerializer(serializers.ModelSerializer):

    created_by = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'], required=False)
    payment = serializers.SerializerMethodField()

    def get_payment(self,obj):
        if hasattr(obj,'payment'):
            if obj.payment is not None:
                  return {'amount' : obj.payment.amount/100, 'status' : obj.payment.status, 'url' : obj.payment.payment_url }

    class Meta:
        model = ServiceClient
        fields = '__all__'

class ServiceClientsCreateSerializer(serializers.ModelSerializer):

    payment = serializers.SerializerMethodField()

    def get_payment(self,obj):
        if hasattr(obj,'payment'):
            if obj.payment is not None:
                if hasattr(obj.payment,'payment_url'):
                    return obj.payment.payment_url

    class Meta:
        model = ServiceClient
        exclude = ['payment','payed','balance']


class ServiceExpertInfoSerializer(serializers.ModelSerializer):


    toss = serializers.SerializerMethodField()

    def get_toss(self,obj):
        lis = []
        toss = ServiceToss.objects.all().last()
        for x in toss.toss.all():
            lis.append({'id': x.id,'title' : x.title})
        return lis

    class Meta:
        model = ServiceExpert
        fields = ['first_name','last_name','toss']

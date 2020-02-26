from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):

    date_created = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'],required=False, source='date_updated')
    date_updated = serializers.DateTimeField(required=False)


    class Meta:
        model = Payment
        fields = ['amount','order_obj','order_plural','success','error_code','payment_url','message','status', 'date_created', 'payment_id','date_updated']

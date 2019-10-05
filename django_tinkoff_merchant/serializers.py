from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ['amount','order_obj','order_plural','success','error_code','payment_url','message','status']

from rest_framework import serializers
from .models import PromoCode

class PromoCodesSerializer(serializers.ModelSerializer):

    class Meta:
        model = PromoCode
        fields = '__all__'

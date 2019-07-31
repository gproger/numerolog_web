
from rest_framework import serializers
from .models import AppOrder

class AppOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppOrder
        fields = '__all__'

class AppWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppOrder
        fields = '__all__'

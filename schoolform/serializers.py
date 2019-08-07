from rest_framework import serializers
from .models import SchoolAppForm, SchoolAppFlow


class SchoolAppFormSerializer(serializers.ModelSerializer):
    bid = serializers.DateField(format="%d.%m.%Y",input_formats=['%d.%m.%Y'])

    class Meta:
        model = SchoolAppForm
        exclude = ['flow']


class SchoolAppFlowSerializer(serializers.ModelSerializer):

    class Meta:
        model = SchoolAppFlow
        fields = '__all__'

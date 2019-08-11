from rest_framework import serializers
from .models import SchoolAppForm, SchoolAppFlow


class SchoolAppFormSerializer(serializers.ModelSerializer):
    bid = serializers.DateField(format="%d.%m.%Y",input_formats=['%d.%m.%Y'])
    created = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'])

    class Meta:
        model = SchoolAppForm
        exclude = ['flow']


class SchoolAppFlowListSerializer(serializers.ModelSerializer):
    state = serializers.SerializerMethodField()
    created = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'])

    def get_state(self, obj):
        return obj.get_state_display()

    class Meta:
        model = SchoolAppFlow
        fields = ['state','created','flow']


class SchoolAppFlowSerializer(serializers.ModelSerializer):
    state = serializers.SerializerMethodField()
    created = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'])

    def get_state(self, obj):
        return obj.get_state_display()

    class Meta:
        model = SchoolAppFlow
        fields = '__all__'

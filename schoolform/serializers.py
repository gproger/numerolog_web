from rest_framework import serializers
from .models import SchoolAppForm, SchoolAppFlow


class SchoolAppFormSerializer(serializers.ModelSerializer):
    bid = serializers.DateField(format="%d.%m.%Y",input_formats=['%d.%m.%Y'])
    created = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'], required=False)

    class Meta:
        model = SchoolAppForm
        exclude = ['flow']


class SchoolAppFlowListSerializer(serializers.ModelSerializer):
    state = serializers.SerializerMethodField()
    created = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'],required=False)

    def get_state(self, obj):
        return obj.get_state_display()

    class Meta:
        model = SchoolAppFlow
        fields = ['state','created','flow']


class SchoolAppFlowSerializer(serializers.ModelSerializer):
#    state = serializers.SerializerMethodField(required=False)
    state = serizliers.ChoiceField(SchollAppFlow.STATES)
    created = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'], required=False)
    price = models.IntegerField(default=30000, required = False)

#   recruitment fields
    toss = models.ManyToManyField(required = False)
    recruitment_start = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y'] , required = False)
    recruitment_stop = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y'] , required = False)

#   started fields
    education_start = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y'] , required = False)
    education_stop = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y'] , required = False)


    def get_state(self, obj):
        return obj.get_state_display()

    class Meta:
        model = SchoolAppFlow
        fields = '__all__'

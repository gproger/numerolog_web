from rest_framework import serializers
from .models import SchoolTraining
from .models import SchoolLesson
from django.urls import reverse
from schoolform.models import SchoolAppCurator

class SchoolTraingListSerializer(serializers.ModelSerializer):
    
    flow = serializers.SerializerMethodField(required=False)

    def get_flow(self, obj):
        return ' ' + str(obj.flow.flow) + ' ' + obj.flow.flow_name

    class Meta:
        model = SchoolTraining
        fields = ['name','id','flow']


class SchoolTraingSerializer(serializers.ModelSerializer):

    curators_list = serializers.SerializerMethodField(required=False)
    curators = serializers.PrimaryKeyRelatedField(queryset=SchoolAppCurator.objects.all(),many=True)

    def get_curators_list(self,obj):
        result = []
        for curator in obj.flow.schoolappcurator_set.filter(curator=True):
            result.append({'id':curator.id,'phone':curator.phone,'first_name':curator.first_name,'last_name':curator.last_name})
        return result

    class Meta:
        model = SchoolTraining
        fields = ['name','curators','curators_list','flow']



class SchoolLessonListSerializer(serializers.ModelSerializer):

    time_start = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y %H:%M:%S'], required=False)

    class Meta:
        model = SchoolLesson
        fields = ['name','id','descr','time_start']

class SchoolLessonCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = SchoolLesson
        fields = ['name','training']


class SchoolLessonSerializer(serializers.ModelSerializer):

    time_start = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y %H:%M:%S'], required=False)

    class Meta:
        model = SchoolLesson
        fields = '__all__'

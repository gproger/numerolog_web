from rest_framework import serializers
from .models import SchoolTraining
from .models import SchoolLesson
from django.urls import reverse

class SchoolTraingListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SchoolTraining
        fields = ['name','id']


class SchoolTraingSerializer(serializers.ModelSerializer):

    curators_list = serializers.SerializerMethodField(required=False)

    def get_curators_list(self,obj):
        result = []
        for curator in obj.flow.schoolappcurator_set.filter(curator=True):
            result.append({'id':curator.id,'phone':curator.phone,'first_name':curator.first_name,'last_name':curator.last_name})
        return result

    class Meta:
        model = SchoolTraining
        fields = ['name','curators','curators_list']



class SchoolLessonListSerializer(serializers.ModelSerializer):

    class Meta:
        model = SchoolLesson
        fields = '__all__'

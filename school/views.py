from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, BasePermission
from rest_framework.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .serializers import SchoolTraingListSerializer
from .serializers import SchoolTraingSerializer
from .serializers import SchoolLessonListSerializer
from .serializers import SchoolLessonSerializer
from .serializers import SchoolLessonCreateSerializer
from .models import SchoolTraining
from .models import SchoolLesson
from schoolform.models import SchoolAppFlow
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect, JsonResponse
import json

# Create your views here.

class SchoolTrainingList(generics.ListCreateAPIView):
    serializer_class = SchoolTraingSerializer
    queryset = SchoolTraining.objects.all()

    def list(self, request):

        query_params = request.query_params
        flow_num = query_params.get('flow', None)


        if flow_num is None:
            return HttpResponseBadRequest()

        queryset = self.get_queryset()
        if flow_num != '0':
            queryset = queryset.filter(flow__id=flow_num)

        serializer = SchoolTraingListSerializer(queryset, many=True)
        return Response(serializer.data)


class SchoolTrainingCreateCopyView(View):
    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        json_data = json.loads(request.body.decode('utf-8'))
        flow = get_object_or_404(SchoolAppFlow,id=json_data['flow_id'])
        copy_obj  = get_object_or_404(SchoolTraining,id=json_data['copy'])
        name = json_data['name']

        sc = SchoolTraining()
        sc.flow = flow
        sc.name = name
        sc.save()
        qs = SchoolLesson.objects.filter(training=copy_obj)
        for item in qs:
            c_item = SchoolLesson()
            c_item.training = sc
            c_item.name = item.name
            c_item.descr = item.descr
            c_item.time_start = item.time_start
            c_item.has_homework = item.has_homework
            c_item.homework_html = item.homework_html
            c_item.lesson_content = item.lesson_content
            c_item.save()
        return JsonResponse({'status':'Done'})



class SchoolTrainingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SchoolTraingSerializer

    def get_object(self):
        id = self.kwargs.get('id', None)
        return get_object_or_404(SchoolTraining,pk=id)



class SchoolLessonList(generics.ListCreateAPIView):
    serializer_class = SchoolLessonCreateSerializer
    queryset = SchoolLesson.objects.all()

    def list(self, request):

        query_params = request.query_params
        tr_id = query_params.get('training', None)

        if tr_id is None:
            return HttpResponseBadRequest()

        queryset = self.get_queryset()
        queryset = queryset.filter(training__id=tr_id)
        serializer = SchoolLessonListSerializer(queryset, many=True)
        return Response(serializer.data)



class SchoolLessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SchoolLessonSerializer

    def get_object(self):
        id = self.kwargs.get('id', None)
        return get_object_or_404(SchoolLesson,pk=id)

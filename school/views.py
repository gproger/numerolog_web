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
from .models import SchoolTraining
from .models import SchoolLesson

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
        queryset = queryset.filter(flow__id=flow_num)
        serializer = SchoolTraingListSerializer(queryset, many=True)
        return Response(serializer.data)

class SchoolTrainingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SchoolTraingSerializer

    def get_object(self):
        id = self.kwargs.get('id', None)
        return get_object_or_404(SchoolTraining,pk=id)





class SchoolLessonList(generics.ListCreateAPIView):
    serializer_class = SchoolLessonListSerializer
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




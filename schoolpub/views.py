from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import SchoolLandingPage
from rest_framework import generics
from rest_framework import permissions
from .models import SchoolTextReviewsPage
from .models import SchoolFAQPage
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response



from .serializers import SchoolTextReviewsSerializer
from .serializers import SchoolFaqSerializer


class SchoolPubView(TemplateView):
    template_name="index1.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page']=SchoolLandingPage.objects.first()
        return context

#from .views import SchoolFaqPubView
#from .views import SchoolReviewPubView



class SchoolFaqPubView(generics.ListAPIView):
    serializer_class = SchoolFaqSerializer
    permission_classes = [permissions.AllowAny]
    queryset = SchoolFAQPage.objects.all().filter(live=True)

    def get_serializer_context(self):
        return {'request': self.request}


class SchoolReviewPubView(generics.ListAPIView):
    serializer_class = SchoolTextReviewsSerializer
    permission_classes = [permissions.AllowAny]
    queryset = SchoolTextReviewsPage.objects.all().filter(live=True)

    def get_serializer_context(self):
        return {'request': self.request}



# Create your views here.

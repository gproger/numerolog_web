from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import SchoolLandingPage

class SchoolPubView(TemplateView):
    template_name="index1.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page']=SchoolLandingPage.objects.first()
        print(context)
        return context

# Create your views here.

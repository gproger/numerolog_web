from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.views import serve
from django.views.generic import TemplateView, RedirectView
from .views import SchoolPubView


urls = [
    url(r'^school/$',SchoolPubView.as_view()),
]

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.views import serve
from django.views.generic import TemplateView, RedirectView
from .views import SchoolPubView
from .views import SchoolFaqPubView
from .views import SchoolReviewPubView


urls = [
    url(r'^school/$',SchoolPubView.as_view()),
    url(r'^numer/api/index/faq/$', SchoolFaqPubView.as_view()),
    url(r'^numer/api/index/review/$', SchoolReviewPubView.as_view()),

]

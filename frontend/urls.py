from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.views import serve
from django.views.generic import TemplateView

urls = [
#    url(r'^$',serve,{'path':'index.html'}),
    url(r'^$',TemplateView.as_view(template_name='index.html')),
    url(r'^chat/$',TemplateView.as_view(template_name='index.html')),
    url(r'^blog/$',TemplateView.as_view(template_name='index.html')),
    url(r'^matrix/$',TemplateView.as_view(template_name='index.html')),    
    url(r'^services/$',TemplateView.as_view(template_name='index.html')),
    url(r'^profile/$',TemplateView.as_view(template_name='index.html')),
    url(r'^profile/user/$',TemplateView.as_view(template_name='index.html')),

]

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.views import serve
from django.views.generic import TemplateView, RedirectView

urls = [
#    url(r'^$',serve,{'path':'index.html'}),
#    url(r'^$',TemplateView.as_view(template_name='index.html')),
    url(r'^$',RedirectView.as_view(url="/school/")),
#RedirectView.as_view(url=reverse_lazy('my_named_pattern')
    url(r'^chat/',TemplateView.as_view(template_name='index.html')),
    url(r'^blog/',TemplateView.as_view(template_name='index.html')),
    url(r'^matrix/',TemplateView.as_view(template_name='index.html')),
    url(r'^services/',TemplateView.as_view(template_name='index.html')),
    url(r'^profile/',TemplateView.as_view(template_name='index.html')),
    url(r'^tos/',TemplateView.as_view(template_name='index.html')),
    url(r'^admin/school/*',TemplateView.as_view(template_name='index.html')),
    url(r'^school/*',TemplateView.as_view(template_name='index.html')),
    url(r'^options/',TemplateView.as_view(template_name='index.html')),
    url(r'^forgotten-password/',TemplateView.as_view(template_name='index.html')),
    url(r'^pay/*',TemplateView.as_view(template_name='index.html')),
    url(r'^serv_pay/*',TemplateView.as_view(template_name='index.html')),
    url(r'^expert/*',TemplateView.as_view(template_name='index.html')),
    url(r'^userInfo/*',TemplateView.as_view(template_name='index.html')),
    url(r'^ticket/*',TemplateView.as_view(template_name='index.html')),
    url(r'^sale/*',TemplateView.as_view(template_name='index.html')),
    url(r'^admin/experts/*',TemplateView.as_view(template_name='index.html')),
    url(r'^admin/events/*',TemplateView.as_view(template_name='index.html')),

]

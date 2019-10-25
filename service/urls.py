from django.conf.urls import url
from .views import ServiceExpertListView, ServiceClientListView
from .views import ServiceClientCreateView
from .views import ServiceExpertInfoView
from .views import ServiceExpertsClientListView
from .views import ServiceExpertsClearBalanceView

urls = [
    url(r'^numer/api/experts/$', ServiceExpertListView.as_view()),
    url(r'^numer/api/expclients/(?P<id>[0-9]+)/$',ServiceExpertsClientListView.as_view()),
    url(r'^numer/api/cl_exp/(?P<id>[0-9]+)/$',ServiceExpertsClearBalanceView.as_view()),
    url(r'^numer/api/clients/(?P<id>[0-9]+)/$',ServiceClientListView.as_view()),
    url(r'^numer/api/exp_add/(?P<slug>[-\w]+)/$',ServiceExpertInfoView.as_view()),
    url(r'^numer/api/pay_to/(?P<slug>[-\w]+)/$',ServiceClientCreateView.as_view()),
]



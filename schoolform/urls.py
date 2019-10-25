from django.conf.urls import url
from .views import SchoolAppFormListView, SchoolAppFlowListView, SchoolAppFormCreateView, SchoolAppCuratorCreateView
from .views import SchoolAppFlowView, SchoolAppFlowRecruitmentListView
from .views import SchoolAppFormShowUpdateView
from .views import SchoolAppFormShowUpdateURLView

urls = [
    url(r'^numer/api/flow/$', SchoolAppFlowListView.as_view()),
    url(r'^numer/api/fdesc/(?P<id>[0-9]+)/$',SchoolAppFlowView.as_view()),
    url(r'^numer/api/schoolflow', SchoolAppFormListView.as_view()),
    url(r'^numer/api/addrecord', SchoolAppFormCreateView.as_view()),
    url(r'^numer/api/addcurator', SchoolAppCuratorCreateView.as_view()),
    url(r'^numer/api/recr_flow', SchoolAppFlowRecruitmentListView.as_view()),
    url(r'^numer/api/school/(?P<id>[0-9]+)/$', SchoolAppFormShowUpdateView.as_view()),
    url(r'^numer/api/schoolurl/(?P<id>[0-9]+)/$', SchoolAppFormShowUpdateURLView.as_view()),
]

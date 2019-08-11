from django.conf.urls import url
from .views import SchoolAppFormListView, SchoolAppFlowListView, SchoolAppFormCreateView
from .views import SchoolAppFlowView

urls = [
    url(r'^numer/api/flow', SchoolAppFlowListView.as_view()),
    url(r'^numer/api/flowdesc/',SchoolAppFlowView.as_view()),
    url(r'^numer/api/schoolflow', SchoolAppFormListView.as_view()),
    url(r'^numer/api/addrecord', SchoolAppFormCreateView.as_view()),
]



from django.conf.urls import url
from .views import PostPageListView
from .views import ServicesListView
from .views import TermsOfServiceView
from .views import TermsOfServiceListView

urls = [
    url(r'^wgtail/api/postpage/$', PostPageListView.as_view()),
    url(r'^wgtail/api/services/$', ServicesListView.as_view()),
    url(r'^wgtail/api/terms/(?P<pk>[0-9]+)/$', TermsOfServiceView.as_view()),
    url(r'^wgtail/api/allterms/$', TermsOfServiceListView.as_view()),
]

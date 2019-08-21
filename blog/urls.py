from django.conf.urls import url
from .views import PostPageListView
from .views import ServicesListView
from .views import TermsOfServiceView

urls = [
    url(r'^wgtail/api/postpage/$', PostPageListView.as_view()),
    url(r'^wgtail/api/services/$', ServicesListView.as_view()),
    url(r'^wgtail/api/terms/(?P<id>[0-9]+)/$', TermsOfServiceView.as_view()),
]

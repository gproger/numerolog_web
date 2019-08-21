from django.conf.urls import url
from .views import PostPageListView
from .views import ServicesListView

urls = [
    url(r'^wgtail/api/postpage', PostPageListView.as_view()),
    url(r'^wgtail/api/services', ServicesListView.as_view()),
]

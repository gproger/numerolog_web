from django.conf.urls import url
from .views import PostPageListView

urls = [
    url(r'^wgtail/api/postpage', PostPageListView.as_view()),
]

from django.conf.urls import url
from .views import CommentsPageListView

urls = [
    url(r'^post/api/comments/(?P<id>[0-9]+)/$', CommentsPageListView.as_view()),
]

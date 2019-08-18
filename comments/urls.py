from django.conf.urls import url
from .views import CommentsPageListView
from .views import CommentAddView
from .views import CommentAddReplyView


urls = [
    url(r'^post/api/comments/(?P<id>[0-9]+)/add', CommentAddView.as_view()),
    url(r'^post/api/comments/(?P<id>[0-9]+)/reply', CommentAddReplyView.as_view()),
    url(r'^post/api/comments/(?P<id>[0-9]+)/$', CommentsPageListView.as_view()),
]

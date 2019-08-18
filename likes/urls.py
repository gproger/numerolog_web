from django.conf.urls import url
#from .views import CommentsPageListView
#from .views import CommentAddView
from .views import LikeReplyAdd
from .views import LikeCommentAdd
from .views import LikePostAdd

urls = [
#    url(r'^likes/api/comments/(?P<id>[0-9]+)/add', CommentAddView.as_view()),
#    url(r'^likes/api/comments/(?P<id>[0-9]+)/reply', CommentAddReplyView.as_view()),
    url(r'^likes/api/reply/(?P<id>[0-9]+)/$', LikeReplyAdd.as_view()),
    url(r'^likes/api/comment/(?P<id>[0-9]+)/$', LikeCommentAdd.as_view()),
    url(r'^likes/api/post/(?P<id>[0-9]+)/$', LikePostAdd.as_view()),
]

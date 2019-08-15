from django.db import models
from django.contrib.auth import get_user_model
from comments.models import Comment, CommentReply
from blog.models import PostPage
# Create your models here.

class LikePost(models.Models):
    post = models.OneToOneField(PostPage,related_name='likes')
    cnt = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(get_user_model(),related_name='liked_posts')

class LikeComment(models.Models):
    comment = models.OneToOneField(Comment,related_name='likes')
    cnt = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(get_user_model(),related_name='liked_comment')

class LikeReply(models.Models):
    reply = models.OneToOneField(CommentReply,related_name='likes')
    cnt = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(get_user_model(),related_name='liked_reply')


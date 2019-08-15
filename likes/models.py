from django.db import models
from django.contrib.auth import get_user_model
from comments.models import Comment, CommentReply
# Create your models here.

class LikePost(models.Model):
    post = models.OneToOneField('blog.PostPage',related_name='likes')
    cnt = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(get_user_model(),related_name='liked_posts')

class LikeComment(models.Model):
    comment = models.OneToOneField(Comment,related_name='likes')
    cnt = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(get_user_model(),related_name='liked_comment')

class LikeReply(models.Model):
    reply = models.OneToOneField(CommentReply,related_name='likes')
    cnt = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(get_user_model(),related_name='liked_reply')


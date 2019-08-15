from django.db import models
from django.contrib.auth import get_user_model
from blog.models import PostPage

# Create your models here.
class CommentBlogThread(models.Model):
    post = models.OneToOneField(PostPage,related_name='comments')


class Comment(models.Model):
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model()
    )
    thread = models.ForeignKey(CommentBlogThread,related_name='comment')


class CommentReply(models.Modes):
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model()
    )
    comment=models.ForeignKey(Comment,related_name='reply')






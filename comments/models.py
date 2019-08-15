from django.db import models
from django.contrib.auth import get_user_model
from wagtail.api import APIField

# Create your models here.
class CommentBlogThread(models.Model):
    post = models.OneToOneField('blog.PostPage',related_name='comments')
    cnt = models.PositiveIntegerField(default=0)

    api_fields = [
	APIField('comment')
    ]

class Comment(models.Model):
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    cnt = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(
        get_user_model()
    )
    thread = models.ForeignKey(CommentBlogThread,related_name='comment')


class CommentReply(models.Model):
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model()
    )
    comment=models.ForeignKey(Comment,related_name='reply')






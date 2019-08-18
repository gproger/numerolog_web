from django.db import models
from django.contrib.auth import get_user_model
from wagtail.api import APIField

# Create your models here.
class CommentBlogThread(models.Model):
    post = models.OneToOneField('blog.PostPage',related_name='comments')
    cnt = models.PositiveIntegerField(default=0)


class Comment(models.Model):
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    cnt = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(
        get_user_model()
    )
    thread = models.ForeignKey(CommentBlogThread,related_name='comment')

    def save(self, *args, **kwargs):
        if self.pk is None:
            'Possible race condition on db access on save'
            self.thread.cnt = self.thread.cnt + 1
            self.thread.save( update_fields=['cnt'])
        super(Comment,self).save(*args, **kwargs)


class CommentReply(models.Model):
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model()
    )
    comment=models.ForeignKey(Comment,related_name='reply')

    def save(self, *args, **kwargs):
        if self.pk is None:
            'Possible race condition on db access on save'
            self.comment.cnt = self.comment.cnt + 1
            self.comment.save(update_fields=['cnt'])
            print(self.comment.thread.cnt)
            self.comment.thread.cnt = self.comment.thread.cnt + 1
            print(self.comment.thread.cnt)
            self.comment.thread.save(update_fields=['cnt'])
            print(self.comment.thread.cnt)
        super(CommentReply,self).save(*args, **kwargs)

from django.contrib import admin
from .models import CommentBlogThread, CommentReply, Comment

admin.site.register(CommentBlogThread)
admin.site.register(CommentReply)
admin.site.register(Comment)

# Register your models here.

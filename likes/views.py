from django.shortcuts import render

from rest_framework import generics
from rest_framework import permissions
from .serializers import LikeReplyAddSerializer
from .serializers import LikeCommentAddSerializer
from .serializers import LikePostAddSerializer
from blog.models import PostPage


class LikeReplyAdd(generics.CreateAPIView):
    serializer_class = LikeReplyAddSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        print(self.kwargs)
        pp_pk = self.kwargs.get('id',None)
        if pp_pk is None:
            return Comment.objects.none()
        try:
            pp = Comment.objects.get(pk=pp_pk)
        except Comment.DoesNotExist:
            return Comment.objects.none()

        return pp.comments.comment.all()

    def get_serializer_context(self):
        pp_pk = self.kwargs.get('id',None)

        return {'request': self.request,'id' : pp_pk}


class LikeCommentAdd(generics.CreateAPIView):
    serializer_class = LikeCommentAddSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        print(self.kwargs)
        pp_pk = self.kwargs.get('id',None)
        if pp_pk is None:
            return Comment.objects.none()
        try:
            pp = Comment.objects.get(pk=pp_pk)
        except Comment.DoesNotExist:
            return Comment.objects.none()

        return pp.likes

    def get_serializer_context(self):
        pp_pk = self.kwargs.get('id',None)

        return {'request': self.request,'id' : pp_pk}

class LikePostAdd(generics.CreateAPIView):
    serializer_class = LikePostAddSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        print(self.kwargs)
        pp_pk = self.kwargs.get('id',None)
        if pp_pk is None:
            return PostPage.objects.none()
        try:
            pp = PostPage.objects.get(pk=pp_pk)
        except PostPage.DoesNotExist:
            return PostPage.objects.none()


    def get_serializer_context(self):
        pp_pk = self.kwargs.get('id',None)
        postPage = PostPage.objects.get(pk=pp_pk)

        return {'request': self.request,'postPage' : postPage}



# Create your views here.

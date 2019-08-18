from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from .serializers import CommentSerializer
from .serializers import CommentAddSerializer
from .serializers import CommentAddReplySerializer

from rest_framework import generics
from rest_framework import permissions
from blog.models import PostPage
from .models import Comment
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CommentsPagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'limit'
    max_page_size = 40

    def get_paginated_response(self, data):
        print('paginated response')
        print(data)
        print('response')
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'page_size': self.page_size,
            'results': data
        })

class CommentsPageListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]
    ordering = ['date']
    pagination_class = CommentsPagePagination

    def get_queryset(self):
        print(self.kwargs)
        pp_pk = self.kwargs.get('id',None)
        if pp_pk is None:
            return Comment.objects.none()
        try:
            pp = PostPage.objects.get(pk=pp_pk)
        except PostPage.DoesNotExist:
            return Comment.objects.none()

        if not hasattr(pp,'comments'):
            return Comment.objects.none()

        if not hasattr(pp.comments,'comment'):
            return Comment.objects.none()

        return pp.comments.comment.all()

    def get_serializer_context(self):
        return {'request': self.request}

class CommentAddView(generics.CreateAPIView):
    serializer_class = CommentAddSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        print(self.kwargs)
        pp_pk = self.kwargs.get('id',None)
        if pp_pk is None:
            return Comment.objects.none()
        try:
            pp = PostPage.objects.get(pk=pp_pk)
        except PostPage.DoesNotExist:
            return Comment.objects.none()

        if not hasattr(pp,'comments'):
            return Comment.objects.none()

        if not hasattr(pp.comments,'comment'):
            return Comment.objects.none()

        return pp.comments.comment.all()

    def get_serializer_context(self):
        p_id = self.kwargs.get('id', None)

        postpage = PostPage.objects.get(pk=p_id)

        return {'request': self.request,'postpage' : postpage}


class CommentAddReplyView(generics.CreateAPIView):
    serializer_class = CommentAddReplySerializer
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
        pp = None
        if pp_pk is None:
            return Comment.objects.none()
        try:
            pp = Comment.objects.get(pk=pp_pk)
        except Comment.DoesNotExist:
            pp = Comment.objects.none()

        return {'request': self.request,'comment' : pp}

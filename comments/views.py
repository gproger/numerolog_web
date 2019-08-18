from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from .serializers import CommentSerializer
from rest_framework import generics
from rest_framework import permissions
from blog.models import PostPage
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CommentsPagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'limit'
    max_page_size = 40

    def get_paginated_response(self, data):
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
        pp_pk = self.kwargs.get('id',None)
        if pp_pk is None:
            return None
        try:
            pp = PostPage.objects.get(pk=pp_pk)
        except PostPage.DoesNotExist:
            return None

        if not hasattr(pp,'comments'):
            return None

        if not hasattr(pp.comments,'comment'):
            return None

        return pp.comments.comment.all()

    def get_serializer_context(self):
        return {'request': self.request}

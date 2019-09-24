from django.shortcuts import render
from .serializers import PostPageCustomSerializer
from .serializers import ServicesCustomSerializer
from .serializers import TermsOfServiceCustomSerializer
from .serializers import TermsOfServiceCustomShortSerializer
from rest_framework import generics
from rest_framework import permissions
from .models import PostPage, ServicePage, TermsOfServicePage
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class PostPagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'limit'
    max_page_size = 1000

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

class PostPageListView(generics.ListAPIView):
    serializer_class = PostPageCustomSerializer
    permission_classes = [permissions.AllowAny]
    queryset = PostPage.objects.all().filter(live=True)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['id', 'last_published_at']
    search_fields = ['@title', '@body']
    ordering = ['-last_published_at']
    pagination_class = PostPagePagination

    def get_serializer_context(self):
        return {'request': self.request}

class ServicesListView(generics.ListAPIView):
    serializer_class = ServicesCustomSerializer
    permission_classes = [permissions.AllowAny]
    queryset = ServicePage.objects.all().filter(live=True)

    def get_serializer_context(self):
        return {'request': self.request}

class TermsOfServiceView(generics.RetrieveAPIView):
    serializer_class = TermsOfServiceCustomSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        pk = self.kwargs.get('pk',None)
        queryset = TermsOfServicePage.objects.filter(pk=pk)
        return queryset

    def get_serializer_context(self):
        return {'request': self.request}

class TermsOfServiceListView(generics.ListAPIView):
    serializer_class = TermsOfServiceCustomShortSerializer
    permission_classes = [permissions.AllowAny]
    queryset = TermsOfServicePage.objects.all()

    

# Create your views here.

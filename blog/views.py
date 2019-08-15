from django.shortcuts import render
from .serializers import PostPageCustomSerializer
from rest_framework import generics
from rest_framework import permissions
from .models import PostPage


class PostPageListView(generics.ListAPIView):
    serializer_class = PostPageCustomSerializer
    permission_classes = [permissions.AllowAny]
    queryset = PostPage.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}

# Create your views here.

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Favorites

from .serializers import FavoritesSerializer


class FavoritesListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FavoritesSerializer

    def list(self, request):
        queryset = Favorites.objects.filter(user=request.user)
        serializer = FavoritesSerializer(queryset, many=True)
        return Response(serializer.data)


class FavoritesDestroyView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FavoritesSerializer

    def get_queryset(self):
        queryset = Favorites.objects.filter(user=self.request.user,
                                            pk=self.kwargs['pk'])
        return queryset

    def perform_destroy(self, instance):
        return instance.delete()

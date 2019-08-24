from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from .models import Favorites

from .serializers import FavoritesSerializer
from .serializers import FavoritesPostAddSerializer

class FavoritesListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FavoritesSerializer

    def list(self, request):
        queryset = Favorites.objects.filter(user=request.user).order_by('-pk')
        serializer = FavoritesSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance=serializer.save()
        instance.user = get_user_model().objects.get(pk=request.user.id)
        instance.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class FavoritesDestroyView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FavoritesSerializer

    def get_queryset(self):
        queryset = Favorites.objects.filter(user=self.request.user,
                                            pk=self.kwargs['pk'])
        return queryset

    def perform_destroy(self, instance):
        return instance.delete()


class FavoritesPostAdd(generics.CreateAPIView):
    serializer_class = FavoritesPostAddSerializer
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

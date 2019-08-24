from django.conf.urls import url
from .views import FavoritesListView, FavoritesDestroyView, FavoritesPostAdd

urls = [
    url(r'^numer/api/favss', FavoritesListView.as_view()),
    url(r'^numer/api/favs/(?P<pk>[0-9]+)', FavoritesDestroyView.as_view()),
    url(r'^numer/api/favpost/(?P<pk>[0-9]+)', FavoritesPostAdd.as_view()),
]

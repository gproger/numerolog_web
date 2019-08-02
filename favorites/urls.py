from django.conf.urls import url
from .views import FavoritesListView, FavoritesDestroyView

urls = [
    url(r'^numer/api/favss', FavoritesListView.as_view()),
    url(r'^numer/api/favs/(?P<pk>[0-9]+)', FavoritesDestroyView.as_view()),
]

from django.contrib import admin
from .models import Favorites, FavoritesPost

# Register your models here.
admin.site.register(Favorites)
admin.site.register(FavoritesPost)


from rest_framework import serializers
from .models import Favorites


class FavoritesSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%d.%m.%Y",input_formats=['%d.%m.%Y'])

    class Meta:
        model = Favorites
        exclude = ['user']

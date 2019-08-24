from rest_framework import serializers
from .models import Favorites, FavoritesPost


class FavoritesSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%d.%m.%Y",input_formats=['%d.%m.%Y'])

    class Meta:
        model = Favorites
        exclude = ['user']



class FavoritesPostAddSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    favs = serializers.SerializerMethodField()

    def get_favs(self,obj):
        if self.context.get('request').user.is_anonymous:
            return False
        return obj.users.filter(id=self.context.get('request').user.id).exists()

    def create(self, validated_data):
        postPage = self.context.get('postPage',None)
        favs = None
        user = self.context.get('request',None).user
        if hasattr(postPage,'favs'):
            favs = postPage.favs
        else:
            favs = FavoritesPost.objects.create(post=postPage)

        if favs.users.filter(id=user.id).exists():
            favs.users.remove(user)
        else:
            favs.users.add(user)

        favs.save()
        return favs

    class Meta:
        model = FavoritesPost
        fields = ['post','favs']


class FavoritesPostSerializer(serializers.ModelSerializer):
    favs = serializers.SerializerMethodField()

    def get_favs(self,obj):
        if self.context.get('request').user.is_anonymous:
            return False
        return obj.users.filter(id=self.context.get('request').user.id).exists()

    class Meta:
        model = FavoritesPost
        fields = ['favs']

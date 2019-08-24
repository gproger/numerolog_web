from rest_framework import serializers
from .models import Favorites, FavoritesPost


class FavoritesSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%d.%m.%Y",input_formats=['%d.%m.%Y'])

    class Meta:
        model = Favorites
        exclude = ['user']



class FavoritesPostAddSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        postPage = self.context.get('postPage',None)
        favs = None
        user = self.context.get('request',None).user
        if hasattr(postPage,'fav_post'):
            favs = postPage.fav_post
        else:
            favs = FavoritesPost.objects.create(post=postPage)

        favs.users.add(user)

        favs.save()
        return favs

    class Meta:
        model = FavoritesPost
        fields = ['post']


class FavoritesPostSerializer(serializers.ModelSerializer):
    favs = serializers.SerializerMethodField()

    def get_favs(self,obj):
        if self.context.get('request').user.is_anonymous:
            return False
        return obj.fav_post.filter(id=self.context.get('request').user.id).exists()

    class Meta:
        model = FavoritesPost
        fields = ['favs']

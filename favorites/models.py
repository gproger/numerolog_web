from django.db import models
from blog.models import PostPage
from django.contrib.auth import get_user_model


class Favorites(models.Model):

    user = models.ForeignKey(
        get_user_model(),
        null=True,
    )
    name = models.CharField(max_length=64, blank=True, null=True)
    date = models.DateField(blank=True, null=True)

class FavoritesPost(models.Model):

    post = models.OneToOneField(
        PostPage,
        related_name='favs'
    )

    users = models.ManyToManyField(get_user_model(),related_name='fav_post')


# Create your models here.

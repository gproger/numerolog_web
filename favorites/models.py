from django.db import models
from django.contrib.auth import get_user_model


class Favorites(models.Model):

    user = models.ForeignKey(
        get_user_model(),
        null=True,
    )
    name = models.CharField(max_length=64, blank=True, null=True)
    date = models.DateField(blank=True, null=True)


# Create your models here.

from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class UserInfo(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    middle_name = models.CharField(max_length=40)
    instagram = models.CharField(max_length=80)
    website = models.URLField(null=True, blank=True)
    bid = models.DateField(null=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.DO_NOTHING, related_name="ninfo")
    phone_valid = models.NullBooleanField(default=False)
### this class used as user info for auth user
### every application in system must be linked to this userinfo

### all SchoolForms 


class UserReviews(models.Model):
    pass



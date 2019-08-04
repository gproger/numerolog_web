from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
import datetime
import random

class AppUser(models.Model):

    email = models.EmailField()
    name = models.CharField(max_length=254, blank=True, null=True)
    code = models.PositiveIntegerField()
    registered = models.BooleanField(default=False)
    valid = models.BooleanField(default=False)
    code_time = models.DateTimeField(auto_now=False, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        """ Add Slug creating/checking to save method.  """
        slug_save(self)
        super(AppUser, self).save(*args, **kwargs)

    def request_new_code(self):
        cur_time = datetime.datetime.now()
        if not self.code_time:
            self.code_time = cur_time
            self.code = random.randrange(100000, 999999)
            # todo add send mail to email
            self.save()
        else:
            timediff = cur_time - self.code_time
            timediff_s = timediff.total_seconds()
            if timediff_s > 180:
                # 3 minutes
                self.code_time = cur_time
                self.code = random.randrange(100000, 999999)
                self.save()
                # todo add send mail to email

#### we need check valid of AppUser - if no valideation in 4 day - we delete registration

    def check_valid(self):
        if self.valid:
            return True

        cur_time = datetime.datetime.now()
        if not self.code_time:
            return True
        timediff = cur_time - self.code_time
        timediff_s = timediff.total_seconds()
        if (timediff_s / 60*24*4) > 1:
            return False


class AppOrder(models.Model):

    number = models.PositiveIntegerField()
    requester = models.ForeignKey(AppUser)
#### ... !!!! MUST BE CHECKED USER STATUS AND PRICE ON CREATE ORDER
    doer = models.ForeignKey(
        get_user_model(),
        null=True,
    )
    created_at = models.DateTimeField()
    deadline_at = models.DateTimeField()
    consult_at = models.DateTimeField()
    items = JSONField()
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        """ Add Slug creating/checking to save method.  """
        slug_save(self)
        super(AppOrder, self).save(*args, **kwargs)

## TODO: add notification to email on create ( or pay? )


# .........
def slug_save(obj):
    if not obj.slug:
        obj.slug = get_random_string(32)
        slug_is_wrong = True
        while slug_is_wrong:
            slug_is_wrong = False
            other_objs_with_slug = type(obj).objects.filter(slug=obj.slug)
            if len(other_objs_with_slug) > 0:
                slug_is_wrong = True
#            naughty_words = list_of_swear_words_brand_names_etc
#            if obj.slug in naughty_words:
#                slug_is_wrong = True
            if slug_is_wrong:
                obj.slug = get_random_string(32)

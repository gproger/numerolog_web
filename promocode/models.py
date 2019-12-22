from django.db import models
from django.contrib.auth import get_user_model
from schoolform.models import SchoolAppFlow, PriceField
# Create your models here.


class PromoCode(models.Model):
    code = models.CharField(max_length=16)
    emitter = models.ForeignKey(get_user_model())
    referal = models.ForeignKey(get_user_model(), blank=True, null=True)
    discount = models.PositiveIntegerField(default=0)
    is_percent = models.NullBooleanField(default=False)
    elapsed_count = models.PositiveIntegerField(default=1)
    flow = models.ForeignKey(SchoolAppFlow, null=True, blank=True)
    price = models.OneToOneField(PriceField, null=True, blank=True)
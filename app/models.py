from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
import datetime
import random
from django_tinkoff_merchant.models import Payment
from django_tinkoff_merchant.services import MerchantAPI
from celery.execute import send_task
from private_storage.fields import PrivateFileField


class AppOrder(models.Model):

    number = models.PositiveIntegerField()
####    requester = models.ForeignKey(AppUser)
    owner = models.ForeignKey(get_user_model(),null=True, related_name='serv_appl_owner')
#### ... !!!! MUST BE CHECKED USER STATUS AND PRICE ON CREATE ORDER
    doer = models.ForeignKey(
        get_user_model(),
        null=True,
        related_name='serv_appl_doer'
    )
    created_at = models.DateTimeField()
    deadline_at = models.DateTimeField()
    consult_at = models.DateTimeField()
    items = JSONField()
    payment = models.ManyToManyField(to=Payment, verbose_name='Payment', blank=True, null=True)
    price = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        """ Add Slug creating/checking to save method.  """
        new = self.pk is None
        super(AppOrder, self).save(*args, **kwargs)
        if new:
            if self.is_autogen:
                self.generate_auto_description()
            else:
                self.send_create_mail_notification()




    @property
    def is_autogen(self):
        return False


    @property
    def first_name(self):
        if hasattr(self.owner,'ninfo'):
            return self.owner.ninfo.first_name
        else:
            return self.owner.get_real_name()

    @property
    def last_name(self):
        return self.owner.ninfo.last_name
    
    @property
    def email(self):
        return self.owner.ninfo.email
    
    @property
    def doer_name(self):
        return self.doer.ninfo.first_name+' '+self.doer.ninfo.last_name
    
    @property
    def phone(self):
        return self.owner.ninfo.phone

    @property
    def payed_amount(self):
        payed = 0
        for p in self.payment.all():
            if p.is_paid():
                payed += p.amount
        return payed // 100 ##self.owner.ninfo.phone



    def send_mail_notification(self):
        send_task('app.tasks.send_create_notification',
                kwargs={"app_id": self.pk})

    def generate_auto_description(self):
        send_task('app.tasks.generate_description',
                kwargs={"app_id": self.pk})


## TODO: add notification to email on create ( or pay? )


class AppResultFile(models.Model):
    title = models.CharField("Title", max_length=200)
    file = PrivateFileField("File", upload_to="apporders/")
    order = models.ForeignKey(AppOrder, on_delete=models.DO_NOTHING,related_name="files")

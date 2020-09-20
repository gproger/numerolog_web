from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
import datetime
import random
from django_tinkoff_merchant.models import Payment
from django_tinkoff_merchant.services import MerchantAPI
from django_tinkoff_merchant.models import TinkoffSettings
from celery.execute import send_task
from private_storage.fields import PrivateFileField

SERVICE_PAYMENT_DESC = 'Оплата разбора психоматрицы экспертом школы неНумерологии Ольги Перцевой'

class AppOrder(models.Model):

    number = models.PositiveIntegerField()
####    requester = models.ForeignKey(AppUser)
    owner = models.ForeignKey(get_user_model(),null=True, related_name='serv_appl_owner')
#### ... !!!! MUST BE CHECKED USER STATUS AND PRICE ON CREATE ORDER
    doer = models.ForeignKey(
        get_user_model(),
        null=True,
        related_name='serv_appl_doer',
        blank=True
    )
    created_at = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
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


    def get_payment_terminal(self):
        return TinkoffSettings.get_services_terminal()


    @property
    def is_autogen(self):
        return 'auto' in self.items


    @property
    def first_name(self):
        if hasattr(self.owner,'ninfo'):
            return self.owner.ninfo.first_name
        else:
            return self.owner.get_real_name()

    @property
    def last_name(self):
        if hasattr(self.owner,'ninfo'):
            return self.owner.ninfo.last_name
        else:
            return ''

    @property
    def email(self):
        return self.owner.ninfo.email
    
    @property
    def doer_name(self):
        if not self.is_autogen:
            return self.doer.ninfo.first_name+' '+self.doer.ninfo.last_name
        else:
            return 'Автоматически'

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

    def check_full_payment(self):
        count = 0
        for payment in self.payment.all():
             if payment.is_paid():
                 count = count + payment.amount
        count /= 100
        if self.price == count and self.is_autogen:
            self.generate_auto_description()

    def send_mail_notification(self):
        send_task('app.tasks.send_create_notification',
                kwargs={"app_id": self.pk})

    def generate_auto_description(self):
         bid = self.items['items'][0]['date']
         bid = bid[-2:]+'.'+bid[5:7]+'.'+bid[0:4]

         send_task('app.tasks.get_automatic_description',
            kwargs={"order_id": self.pk,'bid':bid})


    def create_payment(self, *args, **kwargs):
        order_obj = str(self.pk)
        order_plural="Услуга "
        amount = self.price*100
        if 'amount' in kwargs:
            amount = kwargs.get('amount')

        items = [
            {'name': 'Описание статистической психоматрицы', 'price': amount, 'quantity': 1},
        ]


        payment = Payment(order_obj=order_obj,order_plural=order_plural, amount=amount, description=SERVICE_PAYMENT_DESC,terminal=self.get_payment_terminal()) \
            .with_receipt(email=self.email,phone=self.phone) \
            .with_items(items)

        payment = MerchantAPI().init(payment)

        payment.save()

        self.payment.add(payment)
        self.save()

    def cancel_payment(self, payment):
        return (MerchantAPI().cancel(payment)).save()



## TODO: add notification to email on create ( or pay? )


class AppResultFile(models.Model):
    title = models.CharField("Title", max_length=200)
    file = PrivateFileField("File", upload_to="apporders/")
    order = models.ForeignKey(AppOrder, on_delete=models.DO_NOTHING,related_name="files")

    def save(self, *args, **kwargs):

        new = self.pk is None
        super(AppResultFile, self).save(*args, **kwargs)
        if new:
            self.send_mail_notification()

    def send_mail_notification(self):
        send_task('app.tasks.appResultFileAdded',
                kwargs={"app_id": self.pk})


class AppAutoGeneratorOptions(models.Model):
    url_login = models.URLField(max_length=200)
    url_getDesc = models.URLField(max_length=200)
    username = models.CharField(max_length=200)
    userpass = models.CharField(max_length=200)
    templateid = models.PositiveIntegerField(default=0)



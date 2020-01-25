from django.db import models
from blog.models import TermsOfServicePage
from django_tinkoff_merchant.models import Payment
from django_tinkoff_merchant.services import MerchantAPI
from django.conf import settings

from django_tinkoff_merchant.models import TinkoffSettings
from emails.emails import mail_user

from celery.execute import send_task
# Create your models here.

class PriceField(models.Model):
    price = models.PositiveIntegerField(default=0)
    currency = models.CharField(default='RUB', max_length=7)
    discount = models.PositiveIntegerField(default=0)

class SchoolAppFlow(models.Model):
    STATES = (
        (0, "created"),
        (1, "recruitment"),
        (2, "register"),
        (3, "started"),
        (4, "finished")
    )

    flow = models.PositiveIntegerField()
    flow_name = models.CharField(max_length=255, null=True, blank=True)
    state = models.IntegerField(choices=STATES, default=0)
    created = models.DateTimeField(auto_now_add=True)
#   education price
    price=models.PositiveIntegerField(default=30000, null=True, blank=True)

#   recruitment fields
    toss = models.ManyToManyField(TermsOfServicePage, null=True, blank=True, related_name='toss+')
    recruitment_start = models.DateField(null=True, blank=True)
    recruitment_stop = models.DateField(null=True, blank=True)

#   started fields
    education_start = models.DateField(null=True, blank=True)
    education_stop = models.DateField(null=True, blank=True)

    pers_cur_price =models.PositiveIntegerField(default=15000)

    cur_toss = models.ManyToManyField(TermsOfServicePage, null=True, blank=True, related_name='cur_toss+')
    pers_cur_toss = models.ManyToManyField(TermsOfServicePage, null=True, blank=True, related_name='pers_toss+')
    avail_by_code = models.NullBooleanField(default=False, blank=True, null=True)
    by_code_hint = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.flow)

class SchoolAppForm(models.Model):

    email = models.EmailField()
    phone = models.CharField(max_length=20)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    middle_name = models.CharField(max_length=40)
    instagramm = models.CharField(max_length=80)
    bid = models.DateField()
    accepted = models.CharField(max_length=40)
    payed_by = models.CharField(max_length=240, blank=True, null=True)
    payed_outline = models.PositiveIntegerField(default=0, null=True, blank=True)
    flow = models.ForeignKey(SchoolAppFlow)
    created = models.DateTimeField(auto_now_add=True)
    accepted_toss = models.ManyToManyField(TermsOfServicePage)
    payment = models.ManyToManyField(to=Payment, verbose_name='Payment', blank=True, null=True)
    price = models.PositiveIntegerField(default = 0)
    price_f = models.OneToOneField(PriceField, null=True, blank=True)
    pay_url_sended = models.NullBooleanField(default=False)

    def save(self, *args, **kwargs):

        new = self.pk is None
        if new:
            self.price = self.flow.price
        super(SchoolAppForm, self).save(*args, **kwargs)
        if new:
            self.send_mail_notification()

    def create_payment(self, *args, **kwargs):
        order_obj = str(self.pk)
        order_plural="Школа "
        amount = self.price*100
        if 'amount' in kwargs:
            amount = kwargs.get('amount')

        items = [
            {'name': 'Обучение в школе неНумерологии', 'price': amount, 'quantity': 1},
        ]


        payment = Payment(order_obj=order_obj,order_plural=order_plural, amount=amount, description='Оплата обучения в школе неНумерологии Ольги Перцевой',terminal=TinkoffSettings.get_school_terminal()) \
            .with_receipt(email=self.email,phone=self.phone) \
            .with_items(items)

        payment = MerchantAPI().init(payment)

        payment.save()

        self.payment.add(payment)
        self.save()


    def get_payment_status(self):
        for payment in  self.payment.all():
             if payment.status != 'CONFIRMED':
                 MerchantAPI().status(payment).save()

    def cancel_payment(self):

        return MerchantAPI().cancel(self.payment)

    def send_mail_notification(self):
        send_task('schoolform.send_school_form_pay_url',
                kwargs={"form_id": self.pk})


    def __str__(self):
        return "{} {} {} {} {} {}".format(self.flow.flow, self.pk, self.email, self.phone, self.last_name, self.first_name)


class SchoolAppCurator(models.Model):

    email = models.EmailField()
    phone = models.CharField(max_length=20)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    middle_name = models.CharField(max_length=40)
    instagramm = models.CharField(max_length=80)
    bid = models.DateField()
    flow = models.ForeignKey(SchoolAppFlow)
    created = models.DateTimeField(auto_now_add=True)
    accepted_toss = models.ManyToManyField(TermsOfServicePage)
    curator = models.NullBooleanField()
    expert = models.NullBooleanField()

    def save(self, *args, **kwargs):

        new = self.pk is None
        super(SchoolAppCurator, self).save(*args, **kwargs)
        if new:
            self.send_mail_notification()

    def send_mail_notification(self):
        send_task('schoolform.send_school_curator_registered',
                kwargs={"form_id": self.pk})

    def __str__(self):
        if self.curator and not self.expert:
            return "Куратор {} {} {} {} {} {}".format(self.flow.flow, self.pk, self.email, self.phone, self.last_name, self.first_name)
        if self.expert and not self.curator:
            return "Эксперт {} {} {} {} {} {}".format(self.flow.flow, self.pk, self.email, self.phone, self.last_name, self.first_name)
        if self.expert and self.curator:
            return "Эксперт и куратор {} {} {} {} {} {}".format(self.flow.flow, self.pk, self.email, self.phone, self.last_name, self.first_name)


#### NOT USED MODEL!!!!
class SchoolAppWorker(models.Model):
#### NOT USED MODEL!!!!
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    middle_name = models.CharField(max_length=40)
    instagramm = models.CharField(max_length=80)
    bid = models.DateField()
    flow = models.ForeignKey(SchoolAppFlow)
    created = models.DateTimeField(auto_now_add=True)
    accepted_toss = models.ManyToManyField(TermsOfServicePage)
    expert = models.NullBooleanField()
    curator = models.NullBooleanField()

    def save(self, *args, **kwargs):

        new = self.pk is None
        super(SchoolAppWorker, self).save(*args, **kwargs)
        if new:
            self.send_mail_notification()


    def send_mail_notification(self):
        print('asdf')

    def __str__(self):
        return "{} {} {} {} {} {}".format(self.flow.flow, self.pk, self.email, self.phone, self.last_name, self.first_name)


class SchoolAppPersCuratorForm(models.Model):

    email = models.EmailField()
    phone = models.CharField(max_length=20)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    middle_name = models.CharField(max_length=40)
    bid = models.DateField(null=True)
    accepted = models.CharField(max_length=40)
    flow = models.ForeignKey(SchoolAppFlow)
    created = models.DateTimeField(auto_now_add=True)
    accepted_toss = models.ManyToManyField(TermsOfServicePage)
    payment = models.ManyToManyField(to=Payment, verbose_name='Payment', blank=True, null=True)

    def save(self, *args, **kwargs):

        new = self.pk is None
        super(SchoolAppPersCuratorForm, self).save(*args, **kwargs)
        if new:
            self.create_payment()

    def create_payment(self, *args, **kwargs):
        order_obj = str(self.pk)
        order_plural="Школа "
        amount = self.flow.pers_cur_price*100
        if 'amount' in kwargs:
            amount = kwargs.get('amount')

        items = [
            {'name': 'Услуга персонального куратора  в школе неНумерологии', 'price': amount, 'quantity': 1},
        ]


        payment = Payment(order_obj=order_obj,order_plural=order_plural, amount=amount, description='Услуга персонального куратора  в школе неНумерологии Ольги Перцевой',terminal=TinkoffSettings.get_school_terminal()) \
            .with_receipt(email=self.email,phone=self.phone) \
            .with_items(items)

        payment = MerchantAPI().init(payment)

        payment.save()

        self.payment.add(payment)
        self.save()


    def get_payment_status(self):
        for payment in  self.payment.all():
             if payment.status != 'CONFIRMED':
                 MerchantAPI().status(payment).save()

    def cancel_payment(self):

        return MerchantAPI().cancel(self.payment)

    def __str__(self):
        return "{} {} {} {} {} {}".format(self.flow.flow, self.pk, self.email, self.phone, self.last_name, self.first_name)

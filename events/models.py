from django.db import models
from schoolform.models import PriceField
# Create your models here.
from blog.models import TermsOfServicePage
from django_tinkoff_merchant.models import Payment
from django_tinkoff_merchant.services import MerchantAPI
import datetime
from django.utils.timezone import utc
from emails.emails import mail_user
from django.conf import settings
from django_tinkoff_merchant.models import TinkoffSettings

class OfflineEvent(models.Model):

    description = models.TextField(null=True)
    name = models.CharField(max_length=250)
    address = models.TextField(null=True)
    address_url = models.URLField(null=True)
    ticket_sale_start = models.DateTimeField(null=True)
    ticket_sale_stop = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    toss = models.ManyToManyField(TermsOfServicePage, null=True, blank=True, related_name='oetoss+')


class EventTicketTemplate(models.Model):
    event = models.ForeignKey(OfflineEvent)
    template = models.TextField()
    price = models.PositiveIntegerField()
    name = models.CharField(max_length=250)
    ticket_cnt = models.PositiveSmallIntegerField()
    description = models.TextField()
    per_user_cnt = models.PositiveSmallIntegerField()
    solded_cnt = models.PositiveIntegerField(default=0)

    def get_time_delta_start(self):
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        return (now - self.event.ticket_sale_start).total_seconds()

    def get_time_delta_stop(self):
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        return (self.event.ticket_sale_stop - now).total_seconds()

    def elapsed_count(self):
        return self.ticket_cnt - self.solded_cnt

class Ticket(models.Model):
    eventticket = models.ForeignKey(EventTicketTemplate)
    email = models.EmailField()
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    middle_name = models.CharField(max_length=40)
    phone = models.CharField(max_length=40)
    count = models.PositiveSmallIntegerField(default = 1)
    price_f = models.OneToOneField(PriceField, null=True, blank=True)
    price = models.PositiveIntegerField(default = 0)
    accepted_toss = models.ManyToManyField(TermsOfServicePage)
    payment = models.ManyToManyField(to=Payment, verbose_name='Payment', blank=True, null=True, related_name='ticket')


    def create_payment(self, *args, **kwargs):
        order_obj = str(self.pk)
        order_plural="Встреча "
        amount = self.price*100
        if 'amount' in kwargs:
            amount = kwargs.get('amount')

        items = [
            {'name': 'Участие во встрече с Ольгой Перцевой', 'price': amount, 'quantity': 1},
        ]


        payment = Payment(order_obj=order_obj,order_plural=order_plural, amount=amount, description='Оплата участие во встрече с Ольгой Перцевой',terminal=TinkoffSettings.get_services_terminal()) \
            .with_receipt(email=self.email,phone=self.phone) \
            .with_items(items)

        payment = MerchantAPI(terminal_key=settings.TERMINAL_KEY, secret_key=settings.TERMINAL_SECRET_KEY).init(payment)

        payment.save()

        self.payment.add(payment)
        self.save()


    def get_payment_status(self):
        for payment in  self.payment.all():
             if payment.status != 'CONFIRMED':
                 MerchantAPI(terminal_key=settings.TERMINAL_KEY, secret_key=settings.TERMINAL_SECRET_KEY).status(payment).save()

    def cancel_payment(self):

        return MerchantAPI(terminal_key=settings.TERMINAL_KEY, secret_key=settings.TERMINAL_SECRET_KEY).cancel(self.payment)


    def send_new_ticket_payurl(self):
        context = {
            'url_pay' : settings.MISAGO_ADDRESS+'/pay/pay/ticket/'+str(self.id),
            'user_name' : self.first_name + ' ' + self.last_name,
            "SITE_HOST" : settings.MISAGO_ADDRESS,
        }
#        attach = []
#        ticket = {
#        'filename' : 'ticket.pdf',
#        'file' : None
#        }
#        attach.append(ticket)
        mail_user(self, "Билет на встречу о неНумерологии",'emails/ticket',context=context)


    def save(self, *args, **kwargs):

        new = self.pk is None
        if new:
            self.price = self.eventticket.price

        super(Ticket, self).save(*args, **kwargs)

        if new:
#            self.eventticket.solded_cnt = self.eventticket.solded_cnt + 1
#            self.eventticket.save()
            self.send_new_ticket_payurl()

    def get_amount(self,obj):
        total = 0
        if not hasattr(obj,'payment'):
            return 0
        for k in obj.payment.all():
            if k.status == 'CONFIRMED':
                total += k.amount
        return total/100

    def check_full_payment(self):
        print(self)
        if self.get_amount(self) == self.price:
            print('Full payment detected')
        print('full check payment')

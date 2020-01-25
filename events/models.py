from django.db import models
from schoolform.models import PriceField
# Create your models here.
from blog.models import TermsOfServicePage
from django_tinkoff_merchant.models import Payment
from django_tinkoff_merchant.services import MerchantAPI
import datetime
from django.utils.timezone import utc
from celery.execute import send_task


from django_tinkoff_merchant.models import TinkoffSettings
<<<<<<< HEAD
=======
from .signals import send_ticket_pdf, send_ticket_pay_email
>>>>>>> 25ae0fe4bc9f81f8490e2b2e1f46b5ce19da6fd3

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
            {'name': 'Встрече с Ольгой Перцевой', 'price': amount, 'quantity': 1},
        ]


        payment = Payment(order_obj=order_obj,order_plural=order_plural, amount=amount, description='Встреча с Ольгой Перцевой',terminal=TinkoffSettings.get_services_terminal()) \
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




    def save(self, *args, **kwargs):

        new = self.pk is None
        if new:
            self.price = self.eventticket.price

        super(Ticket, self).save(*args, **kwargs)

        if new:
#            self.eventticket.solded_cnt = self.eventticket.solded_cnt + 1
#            self.eventticket.save()
            if self.price > 0:
<<<<<<< HEAD
                send_task('events.send_new_ticket_payurl',kwargs={ticket_id : self.pk, retry_jitter=True,ignore_result=True})
            else:
                send_task('events.send_ticket_to_email',kwargs={ticket_id : self.pk, retry_jitter=True,ignore_result=True})
=======
                send_ticket_pay_email.send(self.__class__,tick_id=self.pk)
            else:
                send_ticket_pdf.send(self.__class__,tick_id=self.pk)
>>>>>>> 25ae0fe4bc9f81f8490e2b2e1f46b5ce19da6fd3

    def get_amount(self,obj):
        total = 0
        if not hasattr(obj,'payment'):
            return 0
        for k in obj.payment.all():
            if k.status == 'CONFIRMED':
                total += k.amount
        return total/100

    def check_full_payment(self):
        if self.get_amount(self) == self.price:
            self.eventticket.solded_cnt = self.eventticket.solded_cnt + 1
            self.eventticket.save()
<<<<<<< HEAD
            send_task('events.send_ticket_to_email',kwargs={ticket_id : self.pk, retry_jitter=True,ignore_result=True})
=======
            send_ticket_pdf.send(self.__class__,tick_id=self.pk)
>>>>>>> 25ae0fe4bc9f81f8490e2b2e1f46b5ce19da6fd3

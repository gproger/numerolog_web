from django.db import models
from django_tinkoff_merchant.models import Payment
from emails.emails import mail_user
from django.conf import settings
from django.template.defaultfilters import slugify
from blog.models import TermsOfServicePage
from unidecode import unidecode
from django_tinkoff_merchant.models import TinkoffSettings
from django_tinkoff_merchant.services import MerchantAPI
from django_tinkoff_merchant.signals import payment_update
from django.dispatch import receiver

# Create your models here.

class ServiceExpert(models.Model):

    first_name = models.CharField(max_length=40)
    middle_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    phone = models.CharField(max_length=40)
    balance = models.PositiveIntegerField(default=0)
    percent = models.PositiveSmallIntegerField(default=70)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        new = self.pk is None
        super(ServiceExpert, self).save(*args, **kwargs)
        if new:
            self.slug = slugify(unidecode(self.first_name+' '+self.last_name))
            self.save()
            self.send_mail_notification()

    def send_mail_notification(self):
        context = {
            'url_account' : settings.MISAGO_ADDRESS+'/expert/'+str(self.id),
            'user_name' : self.first_name + ' ' + self.last_name,
            'pay_to' : settings.MISAGO_ADDRESS+'/serv_pay/'+self.slug,
            "SITE_HOST" : settings.MISAGO_ADDRESS,
        }
        mail_user(self, "Сайт неНумерологии Ольги Перцевой",'emails/create_expert',context=context)

    def __str__(self):
        return "{} {} {} {} {} {}".format(self.pk, self.email, self.phone, self.last_name, self.first_name, self.balance)



class ServiceClient(models.Model):

    expert = models.ForeignKey(ServiceExpert,related_name='clients')
    first_name = models.CharField(max_length=40)
    middle_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    phone = models.CharField(max_length=40)
    payed = models.NullBooleanField(default=False)
    accepted_toss = models.ManyToManyField(TermsOfServicePage, null=True, blank=True)
    created_by = models.DateTimeField(auto_now=True)
    balance = models.PositiveIntegerField(default=0)

    payment = models.OneToOneField(to=Payment, verbose_name='Payment', blank=True, null=True, related_name='service_client')

    def create_payment(self, amount):
        order_obj = str(self.pk)
        order_plural="Услуга "
        amount = amount*100

        items = [
            {'name': 'Услуги экспертов школы неНумерологии Ольги Перцевой', 'price': amount, 'quantity': 1},
        ]


        payment = Payment(order_obj=order_obj,order_plural=order_plural, amount=amount, description='Оплата обучения в школе неНумерологии Ольги Перцевой', terminal=TinkoffSettings.get_services_terminal()) \
            .with_receipt(email=self.email,phone=self.phone) \
            .with_items(items)

        payment = MerchantAPI(terminal_key=settings.TERMINAL_KEY, secret_key=settings.TERMINAL_SECRET_KEY).init(payment)

        payment.save()

        self.payment = payment
        self.save()

class ServiceToss(models.Model):
    toss = models.ManyToManyField(TermsOfServicePage, null=True, blank=True)


@receiver(payment_update)
def my_handler(sender, **kwargs):
    payment = kwargs.get('payment')
    if payment.status != 'CONFIRMED':
        return

    if hasattr(payment,'service_client'):
        if payment.service_client.payed == False:
            exp = payment.service_client.expert
            print(payment.service_client)
            add_b = (payment.amount) * exp.percent / 100
            payment.service_client.payed = True
            payment.service_client.balance = add_b
            payment.service_client.save()
            exp.balance += add_b

            exp.save()

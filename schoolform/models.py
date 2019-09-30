from django.db import models
from blog.models import TermsOfServicePage
from django_tinkoff_merchant.models import Payment
from django_tinkoff_merchant.services import MerchantAPI
from django.conf import settings
# Create your models here.

class SchoolAppFlow(models.Model):
    STATES = (
        (0, "created"),
        (1, "recruitment"),
        (2, "register"),
        (3, "started"),
        (4, "finished")
    )

    flow = models.PositiveIntegerField()
    state = models.IntegerField(choices=STATES, default=0)
    created = models.DateTimeField(auto_now_add=True)
#   education price
    price=models.PositiveIntegerField(default=30000, null=True, blank=True)

#   recruitment fields
    toss = models.ManyToManyField(TermsOfServicePage, null=True, blank=True)
    recruitment_start = models.DateField(null=True, blank=True)
    recruitment_stop = models.DateField(null=True, blank=True)

#   started fields
    education_start = models.DateField(null=True, blank=True)
    education_stop = models.DateField(null=True, blank=True)


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
    flow = models.ForeignKey(SchoolAppFlow)
    created = models.DateTimeField(auto_now_add=True)
    accepted_toss = models.ManyToManyField(TermsOfServicePage)
    payment = models.OneToOneField(to=Payment, on_delete=models.DO_NOTHING, verbose_name=_('Payment'), blank=True, default = NULL)

    def save(self, *args, **kwargs):
        c_flow = SchoolAppFlow.objects.all().last()
        self.flow = c_flow
        super(SchoolAppForm, self).save(*args, **kwargs)

    def create_payment(self, *args, **kwargs):
        order_id = 'Обучение в школе нумерологии № '
        order_id += str(self.pk)
        items = [
            {'name': 'Обучение в школе нумерологии', 'price': self.flow.price*100, 'quantity': 1},
        ]

        payment = Payment(order_id=order_id, amount=self.flow.price*100) \
            .with_receipt(email=self.email) \
            .with_items(items)

        MerchantAPI(terminal_key=settings.TERMINAL_KEY, secret_key=settings.TERMINAL_SECRET_KEY).init(payment)

        self.payment = payment
        self.save()




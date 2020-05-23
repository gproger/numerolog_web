from django.db import models
from blog.models import TermsOfServicePage
from django_tinkoff_merchant.models import Payment
from django_tinkoff_merchant.services import MerchantAPI
from django.conf import settings

from django_tinkoff_merchant.models import TinkoffSettings
from emails.emails import mail_user
from celery.execute import send_task
import pytz
from datetime import datetime, timedelta
# Create your models here.

PERS_CURATOR_DESC = 'Услуга персонального куратора в школе неНумерологии Ольги Перцевой'
SCHOOL_PAYMENT_DESC = 'Оплата обучения в школе неНумерологии Ольги Перцевой'

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
    slug = models.SlugField(allow_unicode=True)
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return str(self.flow) + ' ' + str(self.flow_name)

class SchoolAppPersCuratorForm(models.Model):

    _email = models.EmailField()
    _phone = models.CharField(max_length=20)
    _first_name = models.CharField(max_length=40)
    _last_name = models.CharField(max_length=40)
    _middle_name = models.CharField(max_length=40)
    _bid = models.DateField(null=True)
    accepted = models.CharField(max_length=40)
    flow = models.ForeignKey(SchoolAppFlow)
    created = models.DateTimeField(auto_now_add=True)
    accepted_toss = models.ManyToManyField(TermsOfServicePage)
    payment = models.ManyToManyField(to=Payment, verbose_name='Payment', blank=True, null=True)

    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, val):
        self._email = val
    
    @property
    def phone(self):
        return self._phone
    
    @phone.setter
    def phone(self, val):
        self._phone = val

    @property
    def first_name(self):
        return self._first_name
    
    @first_name.setter
    def first_name(self, val):
        self._first_name = val

    @property
    def last_name(self):
        return self._last_name
    
    @last_name.setter
    def last_name(self, val):
        self._last_name = val


    @property
    def middle_name(self):
        return self._last_name
    
    @middle_name.setter
    def middle_name(self, val):
        self._middle_name = val

    @property
    def bid(self):
        return self._bid
    
    @bid.setter
    def bid(self, val):
        self._bid = val


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


        payment = Payment(order_obj=order_obj,order_plural=order_plural, amount=amount, description=PERS_CURATOR_DESC,terminal=TinkoffSettings.get_school_terminal()) \
            .with_receipt(email=self.email,phone=self.phone) \
            .with_items(items)

        payment = MerchantAPI().init(payment)

        payment.save()

        self.payment.add(payment)
        self.save()


    def get_payment_status(self):
        for payment in  self.payment.all():
             if not payment.is_paid():
                 MerchantAPI().status(payment).save()

    def cancel_payment(self):

        return MerchantAPI().cancel(self.payment)

    def is_payed(self):
        total = 0
        for payment in self.payment.all():
            if payment.is_paid():
                total += payment.amount
        if total == self.flow.pers_cur_price*100:
            return True
        else:
            return False

    def __str__(self):
        return "{} {} {} {} {} {}".format(self.flow.flow, self.pk, self.email, self.phone, self.last_name, self.first_name)


class SchoolAppForm(models.Model):

    _email = models.EmailField()
    _phone = models.CharField(max_length=20)
    _first_name = models.CharField(max_length=40)
    _last_name = models.CharField(max_length=40)
    _middle_name = models.CharField(max_length=40)
    _instagram = models.CharField(max_length=80)
    _bid = models.DateField()
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
    payed_amount = models.PositiveIntegerField(default=0)
    
    _phone_valid = models.NullBooleanField(default=False)
    _email_valid = models.NullBooleanField(default=False)
    
    comment = models.TextField(null=True, blank=True)


    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, val):
        self._email = val
    
    @property
    def phone(self):
        return self._phone
    
    @phone.setter
    def phone(self, val):
        self._phone = val

    @property
    def first_name(self):
        return self._first_name
    
    @first_name.setter
    def first_name(self, val):
        self._first_name = val

    @property
    def last_name(self):
        return self._last_name
    
    @last_name.setter
    def last_name(self, val):
        self._last_name = val


    @property
    def middle_name(self):
        return self._last_name
    
    @middle_name.setter
    def middle_name(self, val):
        self._middle_name = val

    @property
    def bid(self):
        return self._bid
    
    @bid.setter
    def bid(self, val):
        self._bid = val

    @property
    def instagramm(self):
        return self._instagram
    
    @instagramm.setter
    def instagramm(self, val):
        self._instagram = val

    @property
    def phone_valid(self):
        return self._phone_valid
    
    @phone_valid.setter
    def phone_valid(self, val):
        self._phone_valid = val

    @property
    def email_valid(self):
        return self._email_valid
    
    @email_valid.setter
    def email_valid(self, val):
        self._email_valid = val



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


        payment = Payment(order_obj=order_obj,order_plural=order_plural, amount=amount, description=SCHOOL_PAYMENT_DESC,terminal=TinkoffSettings.get_school_terminal()) \
            .with_receipt(email=self.email,phone=self.phone) \
            .with_items(items)

        d_now = datetime.now().replace(tzinfo=pytz.UTC)


        dt = datetime.combine(self.flow.education_start,datetime.min.time())
        dt = dt.replace(tzinfo=pytz.UTC)

        if d_now > dt:
            dt = d_now + timedelta(days=10)
            dt = dt.replace(hour=0,minute=0,second=0,microsecond=0)
       	    payment = MerchantAPI().init(payment, date_valid=dt.isoformat())
        else:
       	     payment = MerchantAPI().init(payment, date_valid=dt.isoformat())

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
        send_task('schoolform.tasks.send_school_form_pay_url',
                kwargs={"form_id": self.pk})


    def check_full_payment(self):
        count = 0
        for payment in self.payment.all():
             if payment.is_paid():
                 count = count + payment.amount
        count /= 100
        self.payed_amount = count
        self.save()

    def get_curator_form(self):
        forms = SchoolAppPersCuratorForm.objects.filter(flow=self.flow,email=self.email)
        if forms.count() != 0:
            return forms.first()
        return None

    def apply_promocode(self, cc_code):
        # check if code already exist
        if self.price_f is not None:
            return False

        if cc_code is None:
            return False

#        if cc_code is not None:
#            code = PromoCode.objects.filter(flow=self.flow,
#                                            code=cc_code,
#                                            elapsed_count__gte=1)

        if cc_code.flow != self.flow:
            return False
        if cc_code.elapsed_count < 1:
            return False

        code_item = cc_code
        pr_field = PriceField()
        pr_field.price = self.price
        if code_item.is_percent:
            pr_field.discount = pr_field.price*code_item.discount/100
        else:
            pr_field.discount = code_item.discount
        self.price = pr_field.price - pr_field.discount
        pr_field.save()
        self.price_f = pr_field
        self.save()
        code_item.price.add(pr_field)
        code_item.elapsed_count = code_item.elapsed_count - 1
        code_item.save()
        return True

    def __str__(self):
        return "{} {} {} {} {} {}".format(self.flow.flow, self.pk, self.email, self.phone, self.last_name, self.first_name)

    @classmethod
    def get_registered_from_date(cls, date):
        payments = Payment.objects.filter(terminal=TinkoffSettings.get_school_terminal(),date_updated__gte=date)
        objs = []
        for p in payments:
            if p.description != SCHOOL_PAYMENT_DESC:
                continue
            if p.is_paid():
                print(p.order_obj)
                try:
                    obj = SchoolAppForm.objects.get(pk=p.order_obj)
                except SchoolAppForm.DoesNotExist:
                    continue

                amount = obj.payed_amount*100 - p.amount
                if amount == 0:
                    objs.append(obj)
        return objs


class SchoolAppCurator(models.Model):

    _email = models.EmailField()
    _phone = models.CharField(max_length=20)
    _first_name = models.CharField(max_length=40)
    _last_name = models.CharField(max_length=40)
    _middle_name = models.CharField(max_length=40)
    _instagramm = models.CharField(max_length=80)
    _bid = models.DateField()
    flow = models.ForeignKey(SchoolAppFlow)
    created = models.DateTimeField(auto_now_add=True)
    accepted_toss = models.ManyToManyField(TermsOfServicePage)
    curator = models.NullBooleanField()
    expert = models.NullBooleanField()


    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, val):
        self._email = val
    
    @property
    def phone(self):
        return self._phone
    
    @phone.setter
    def phone(self, val):
        self._phone = val

    @property
    def first_name(self):
        return self._first_name
    
    @first_name.setter
    def first_name(self, val):
        self._first_name = val

    @property
    def last_name(self):
        return self._last_name
    
    @last_name.setter
    def last_name(self, val):
        self._last_name = val


    @property
    def middle_name(self):
        return self._last_name
    
    @middle_name.setter
    def middle_name(self, val):
        self._middle_name = val

    @property
    def bid(self):
        return self._bid
    
    @bid.setter
    def bid(self, val):
        self._bid = val

    @property
    def instagramm(self):
        return self._instagram
    
    @instagramm.setter
    def instagramm(self, val):
        self._instagram = val

    def save(self, *args, **kwargs):

        new = self.pk is None
        super(SchoolAppCurator, self).save(*args, **kwargs)
        if new:
            self.send_mail_notification()

    def send_mail_notification(self):
        send_task('schoolform.tasks.send_school_curator_registered',
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

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
from users.models import UserInfo
from private_storage.fields import PrivateFileField

# Create your models here.

PERS_CURATOR_DESC = 'Услуга персонального куратора в школе неНумерологии Ольги Перцевой'
ACCESS_EXTEND_DESC = 'Услуга продления доступа к учебным материалам в школе неНумерологии Ольги Перцевой'
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

    discounts_by_orders = models.ManyToManyField('SchoolDiscount', blank=True, related_name='main_flow')
    terminal = models.ManyToManyField(TinkoffSettings, blank=True, related_name='used_in+')

    program_html = models.TextField(blank=True, null=True)
    extend_price = models.PositiveIntegerField(default=5000)

    getcourse_url = models.URLField(blank=True, null=True)
    getcourse_ext_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return str(self.flow) + ' ' + str(self.flow_name)

    def get_payment_terminal(self):
        if self.terminal.count() > 0:
            return self.terminal.all()[0]
        else:
            return TinkoffSettings.get_school_terminal()


class SchoolDiscount(models.Model):
    flow = models.ForeignKey(SchoolAppFlow)
    discount = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return str(self.flow.flow_name)+' '+str(self.discount)

class SchoolAppPersCuratorForm(models.Model):


    accepted = models.CharField(max_length=40)
    flow = models.ForeignKey(SchoolAppFlow)
    created = models.DateTimeField(auto_now_add=True)
    accepted_toss = models.ManyToManyField(TermsOfServicePage)
    payment = models.ManyToManyField(to=Payment, verbose_name='Payment', blank=True, null=True)
    price = models.PositiveIntegerField(default = 0)
    userinfo = models.ForeignKey(UserInfo, on_delete=models.DO_NOTHING, blank=True, null=True)

    @property
    def email(self):
        return self.userinfo.email
    
    
    @property
    def phone(self):
        return self.userinfo.phone
    

    @property
    def first_name(self):
        return self.userinfo.first_name
    

    @property
    def last_name(self):
        return self.userinfo.last_name


    @property
    def middle_name(self):
        return self.userinfo.last_name
    
    @property
    def bid(self):
        return self.userinfo.bid

    @property
    def payed_amount(self):
        total = 0
        for payment in self.payment.all():
            if payment.is_paid():
                total += payment.amount
        total /= 100
        return total 


    def save(self, *args, **kwargs):

        new = self.pk is None
        super(SchoolAppPersCuratorForm, self).save(*args, **kwargs)

    def create_payment(self, *args, **kwargs):
        order_obj = str(self.pk)
        order_plural="Школа "
        amount = self.price*100
        if 'amount' in kwargs:
            amount = kwargs.get('amount')

        items = [
            {'name': 'Услуга персонального куратора  в школе неНумерологии', 'price': amount, 'quantity': 1},
        ]


        payment = Payment(order_obj=order_obj,order_plural=order_plural, amount=amount, description=PERS_CURATOR_DESC,terminal=self.flow.get_payment_terminal()) \
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
    
    
    comment = models.TextField(null=True, blank=True)

    userinfo = models.ForeignKey(UserInfo, on_delete=models.DO_NOTHING, blank=True, null=True)
    access_till = models.DateField(null=True, blank=True)



    @property
    def email(self):
        return self.userinfo.email
    
    @property
    def phone(self):
        return self.userinfo.phone
    
    @property
    def first_name(self):
        return self.userinfo.first_name

    @property
    def last_name(self):
        return self.userinfo.last_name
    
    @property
    def middle_name(self):
        return self.userinfo.middle_name
    
    @property
    def bid(self):
        return self.userinfo.bid
    
    @property
    def instagramm(self):
        return self.userinfo.instagram
    
    @property
    def phone_valid(self):
        return self.userinfo.phone_valid
    
    @property
    def email_valid(self):
        return self.userinfo.email_valid
    
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


        payment = Payment(order_obj=order_obj,order_plural=order_plural, amount=amount, description=SCHOOL_PAYMENT_DESC,terminal=self.flow.get_payment_terminal()) \
            .with_receipt(email=self.email,phone=self.phone) \
            .with_items(items)

        d_now = datetime.now().replace(tzinfo=pytz.UTC)


        dt = datetime.combine(self.flow.education_start,datetime.min.time())
        dt = dt.replace(tzinfo=pytz.UTC)
        delta = dt-d_now

        if d_now > dt:
            dt = d_now + timedelta(days=10)
            dt = dt.replace(hour=0,minute=0,second=0,microsecond=0)
       	    payment = MerchantAPI().init(payment, date_valid=dt.isoformat())
        else:
            if delta.days > 89:
                dt = d_now + timedelta(days=89)
                dt = dt.replace(hour=0,minute=0,second=0,microsecond=0)
            payment = MerchantAPI().init(payment, date_valid=dt.isoformat())

        payment.save()

        self.payment.add(payment)
        self.save()


    def get_payment_status(self):
        for payment in  self.payment.all():
             if payment.is_paid():
                 MerchantAPI().status(payment).save()

    def cancel_payment(self, payment):

        return (MerchantAPI().cancel(payment)).save()


    def send_mail_notification(self):
        send_task('schoolform.tasks.send_school_form_pay_url',
                kwargs={"form_id": self.pk})

    def send_mail_random_template(self, f_id):
        send_task('schoolform.tasks.send_school_random_mail',
                kwargs={"form_id": self.pk,"random_t_id":f_id})


    def check_full_payment(self):
        count = 0
        for payment in self.payment.all():
             if payment.is_paid():
                 count = count + payment.amount
        count /= 100
        self.payed_amount = count
        self.save()

    def get_curator_form(self):
        forms = SchoolAppPersCuratorForm.objects.filter(flow=self.flow,userinfo=self.userinfo)
        if forms.count() != 0:
            return forms.first()
        return None


    def test_promocode(self, code):
        cc_code = PromoCode.objects.filter(code=code)
        if cc_code is None:
            return 0

        cc_code = cc_code.first()
  
        if cc_code.flow != self.flow:
            return -1

        if cc_code.elapsed_count < 1:
            return -2

        res = self.apply_promocode(cc_code)
        if not res:
            return -3

        if res:
            return 1


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
        payments = Payment.objects.filter(terminal=self.flow.get_payment_terminal(),date_updated__gte=date)
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

    flow = models.ForeignKey(SchoolAppFlow)
    created = models.DateTimeField(auto_now_add=True)
    accepted_toss = models.ManyToManyField(TermsOfServicePage)
    curator = models.NullBooleanField()
    expert = models.NullBooleanField()

    userinfo = models.ForeignKey(UserInfo, on_delete=models.DO_NOTHING, blank=True, null=True)



    @property
    def email(self):
        return self.userinfo.email

    @property
    def phone(self):
        return self.userinfo.phone

    @property
    def first_name(self):
        return self.userinfo.first_name

    @property
    def last_name(self):
        return self.userinfo.last_name
    
    @property
    def middle_name(self):
        return self.userinfo.middle_name


    @property
    def bid(self):
        return self.userinfo.bid


    @property
    def instagramm(self):
        return self.userinfo.instagram
    

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
        return 'Some strange {}'.format(self.id)

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



class SchoolScanFile(models.Model):
    title = models.CharField("Title", max_length=200)
    file = PrivateFileField("File", upload_to="schoolorders/")
    order = models.ForeignKey(SchoolAppForm, on_delete=models.DO_NOTHING,related_name="files")

    def save(self, *args, **kwargs):

        new = self.pk is None
        super(SchoolScanFile, self).save(*args, **kwargs)
        if new:
            self.send_mail_notification()

    def send_mail_notification(self):
        print("sscan file added")
 #       send_task('app.tasks.appResultFileAdded',
 #               kwargs={"app_id": self.pk})




class SchoolExtendAccessService(models.Model):
    form = models.ForeignKey(SchoolAppForm, related_name='extends')
    payment = models.ManyToManyField(to=Payment, verbose_name='Payment', blank=True, null=True)
    price = models.PositiveIntegerField(default = 0)
    access_till = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    userinfo = models.ForeignKey(UserInfo, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='schoolextend')
    payed = models.BooleanField(default=False)

    @property
    def email(self):
        return self.form.userinfo.email

    @property
    def phone(self):
        return self.form.userinfo.phone

    @property
    def first_name(self):
        return self.form.userinfo.first_name

    @property
    def last_name(self):
        return self.form.userinfo.last_name

    @property
    def middle_name(self):
        return self.form.userinfo.middle_name



    def create_payment(self, *args, **kwargs):
        order_obj = str(self.pk)
        order_plural="Школа "
        amount = self.price*100
        if 'amount' in kwargs:
            amount = kwargs.get('amount')

        items = [
            {'name': 'Услуга продления доступа к материалам школы неНумерологии', 'price': amount, 'quantity': 1},
        ]


        payment = Payment(order_obj=order_obj,order_plural=order_plural, amount=amount, description=ACCESS_EXTEND_DESC,terminal=self.form.flow.get_payment_terminal()) \
            .with_receipt(email=self.email,phone=self.phone) \
            .with_items(items)

        payment = MerchantAPI().init(payment)

        payment.save()

        self.payment.add(payment)
        self.save()


    def get_payment_status(self):
        for payment in self.payment.all():
             if not payment.is_paid():
                 MerchantAPI().status(payment).save()

    def cancel_payment(self,payment):
        return (MerchantAPI().cancel(payment)).save()

    def is_payed(self):
        total = 0
        for payment in self.payment.all():
            if payment.is_paid():
                total += payment.amount
        if total == self.flow.pers_cur_price*100:
            return True
        else:
            return False


    @property
    def payed_amount(self):
        total = 0
        for payment in self.payment.all():
            if payment.is_paid():
                total += payment.amount
        total /= 100
        return total 


    def check_full_payment(self):
        if self.payed_amount == self.price and not self.payed:
            self.update_access_date()


    def update_access_date(self):
        date_form = self.form.flow.education_stop
        if self.form.access_till is not None:
            if self.form.access_till > date_form:
                date_form = self.form.access_till

        for payment in self.payment.all():
            if payment.is_paid():
                date_p = payment.date_updated.date()
                if date_p > date_form:
                    date_form = date_p

        date_res = date_form + timedelta(days=31)
        self.access_till = date_res
        self.payed=True
        self.save()
        self.form.access_till = date_res
        self.form.save()


class RandomMail(models.Model):
    text = models.TextField()

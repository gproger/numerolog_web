from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
import datetime
import random
import pytz
from django_tinkoff_merchant.models import Payment
from django_tinkoff_merchant.services import MerchantAPI
from django_tinkoff_merchant.models import TinkoffSettings
from celery.execute import send_task
from private_storage.fields import PrivateFileField
from blog.models import ServicePage

SERVICE_PAYMENT_DESC = 'Оплата разбора психоматрицы экспертом школы неНумерологии Ольги Перцевой'

class AppAutoGeneratorOptions(models.Model):
    url_login = models.URLField(max_length=200)
    url_getDesc = models.URLField(max_length=200)
    username = models.CharField(max_length=200)
    userpass = models.CharField(max_length=200)
    templateid = models.PositiveIntegerField(default=0)
    serv_id = models.PositiveIntegerField(default=0)

class AppExpertUser(models.Model):
    user=models.OneToOneField(get_user_model(), null=True, blank=True,on_delete=models.DO_NOTHING,related_name='expert_rec')
    serial_no=models.CharField(max_length=200,blank=True,null=True)
    balance = models.PositiveIntegerField(default=0)
    percent = models.PositiveSmallIntegerField(default=70)
    slug = models.SlugField()
    active=models.BooleanField(default=False)
    orders_in_work=models.PositiveIntegerField(default=0)
    workstate = JSONField(blank=True, null=True)

    def add_to_history(self, desc):
        if self.workstate is None:
            ws={}
            ws['history']=[]
            self.workstate=ws
            self.save()
        elif not 'history' in self.workstate:
            self.workstate['history']=[]
            self.save()

        ts={}
        ts['date']=datetime.datetime.now().isoformat()
        ts['desc']=desc
        self.workstate['history'].append(ts)
        self.save()


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
    workstate = JSONField(blank=True, null=True)
    name = models.CharField(max_length=200, null=True)
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
            s_id = int(self.items['serv_id'])
            service = ServicePage.objects.get(id=s_id)
            cnt_f = AppAutoGeneratorOptions.objects.filter(serv_id=s_id).count()
            self.name = service.title
            if cnt_f > 0:
                self.items['auto']='True'
            ws={}
            ws['history']=[]
            ts={}
            ts['desc']='Заказ создан'
            ts['date']= datetime.datetime.now().isoformat()
            ws['history'].append(ts)
            self.workstate=ws
            self.save()
            self.create_payment()
            #self.send_create_mail_notification()


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
            if self.doer is None:
                return 'Назначается'
            for item in self.workstate['assign']:
                if item['confirmed']==True:
                    return self.doer.ninfo.first_name+' '+self.doer.ninfo.last_name
            return 'Назначается'
        else:
            return 'Автоматически'

    @property
    def phone(self):
        return self.owner.ninfo.phone

    @property
    def owner_phone(self):
        return self.owner.ninfo.phone

    @property
    def doer_phone(self):
        if not self.doer is None:
            return self.doer.ninfo.phone
        else:
            return '+79687432507'
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
        elif self.price == count:
            self.try_assign_expert()
            

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


    def add_to_history(self, desc):
        if self.workstate is None:
            ws={}
            ws['history']=[]
            self.workstate=ws
            self.save()
        elif not 'history' in self.workstate:
            self.workstate['history']=[]
            self.save()

        ts={}
        ts['date']=datetime.datetime.now().isoformat()
        ts['desc']=desc
        self.workstate['history'].append(ts)
        self.save()


    def need_assign_expert(self):
        if self.doer is not None or self.is_autogen:
            return False
        if not 'assign' in self.workstate:
            return True
        if not isinstance(self.workstate['assign'],list):
            return True
        if len(self.workstate['assign'])==0:
            return True 
        if self.workstate['assign'][-1]['confirmed']:
            return False
        if self.workstate['assign'][-1]['pending']:
            return False
        return True


    def get_expert_for_assign(self):
### returns AppExpert object for send request for order proceed
        exp_used_set=set()
        if self.workstate is not None:
            if 'assign' in self.workstate:
                for item in self.workstate['assign']:
                    exp_used_set.add(item['exp_id'])
        
        qs = AppExpertUser.objects.filter(active=True).exclude(pk__in=exp_used_set).order_by('orders_in_work')
        cnt_qs = qs.count()
        if cnt_qs > 0:
            qs_ind = random.randint(0,cnt_qs-1)
        else:
            return None
        return qs[qs_ind]

    def send_assign_request(self,expert):
        if self.workstate is None:
            self.workstate={}
        if not 'assign' in self.workstate:
            self.workstate['assign']=[]
        ts={}
        ts['exp_id']=expert.id
        ts['datetime']=datetime.datetime.now().isoformat()
        ts['confirmed']=False
        ts['pending']=True
        self.workstate['assign'].append(ts)
        self.doer=expert.user
        self.save()
        self.send_expert_notification(expert.id)

    def try_assign_expert(self):
        tm = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
        if tm.hour>=9 and tm.hour<=24:
            expert = self.get_expert_for_assign()
            if not expert is None:
                self.send_assign_request(expert)

    def send_expert_notification(self, expert_id):
### send sms and email to expert
        send_task('app.tasks.appPendingExpertAssign',
                kwargs={"app_id": self.pk,"exp_id": expert_id})

## TODO: add notification to email on create ( or pay? )
    def change_expert(self):
        self.try_assign_expert()


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
        print("send file added")
        send_task('app.tasks.appResultFileAdded',
                kwargs={"app_id": self.pk})




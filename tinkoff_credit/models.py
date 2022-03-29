from django.db import models
from django.urls import reverse
from decimal import Decimal
from schoolform.models import SchoolAppForm

class TinkoffCreditSettings(models.Model):
    shopId = models.CharField(max_length=250,verbose_name='Shop identifier')
    showcaseid = models.CharField(max_length=250,verbose_name='Site identifier',blank=True, null=True)
    serverips = models.CharField(max_length=18,verbose_name='Tinkoff Servers netmask',default='91.194.226.00/23')
    promoCode = models.CharField(max_length=100,verbose_name='Идентификатор кредитного продукта')


class CreditApplication(models.Model):
    settings = models.ForeignKey(to=TinkoffCreditSettings, on_delete=models.DO_NOTHING,verbose_name='Настройки')
    order_obj = models.CharField(verbose_name='Номер услуги/анкеты',max_length=100, default='None')
    order_type = models.CharField(verbose_name='Название услуги', max_length=100, default='None')
    schoolappform = models.OneToOneField(to=SchoolAppForm, on_delete=models.DO_NOTHING,verbose_name='Школьная анкета',related_name='credit',blank=True, null=True)
    #### items will be defined later in next class
    tcb_id = models.CharField(verbose_name='ID заявки в TCB',max_length=250,blank=True)
    link_url = models.TextField(verbose_name='Ссылка на заявку в TCB',blank=True)
    status = models.CharField(verbose_name='Текущий статус заявки',max_length=40,blank=True)
    created_at = models.DateTimeField(verbose_name='Дата и время создания заявки.',blank=True,null=True)
    demo = models.NullBooleanField(verbose_name='Демо или реальная заявка')
    committed = models.NullBooleanField(verbose_name='Подтверждена ли заявка')
    first_payment = models.DecimalField(verbose_name='Первый платеж',max_digits=15,decimal_places=2, blank=True,null=True)
    order_amount = models.DecimalField(verbose_name='Сумма заказа',max_digits=15,decimal_places=2, default=0,blank=True,null=True)
    product = models.CharField(max_length=100,verbose_name='Тип продукта',blank=True)
    loan_number=models.CharField(max_length=255,verbose_name='Номер договора',blank=True)
    first_name = models.CharField(max_length=100,verbose_name='Имя клиента',blank=True)
    last_name = models.CharField(max_length=100,verbose_name='Фамилия клиента',blank=True)
    middle_name = models.CharField(max_length=100,verbose_name='Отчество клиента',blank=True)
    phone = models.CharField(max_length=15,verbose_name='Номер телефона', blank=True)
    email = models.CharField(max_length=100,verbose_name='Email',blank=True)
    signing_type = models.CharField(max_length=20,verbose_name='Тип подписания', blank=True)

    @property
    def has_persdata(self):
        if not hasattr(self,'first_name'):
            return False
        if not hasattr(self,'last_name'):
            return False
        if not hasattr(self,'middle_name'):
            return False
        if not hasattr(self,'email'):
            return False
        if not hasattr(self,'phone'):
            return False
        if self.first_name is None:
            return False
        if self.last_name is None:
            return False
        if self.middle_name is None:
            return False
        if self.email is None:
            return False
        if self.phone is None:
            return False
        if self.first_name == '':
            return False
        if self.last_name == '':
            return False
        if self.middle_name == '':
            return False
        if self.email == '':
            return False
        if self.phone == '':
            return False
        return True

    @property
    def cutted_phone(self):
        if len(self.phone) < 8:
            return ''
        if self.phone[0] == '+' and self.phone[1] == '7':
            return self.phone[2:]
        return ''

    @property
    def persdata(self):
        return {'contact':{
                'mobilePhone':self.cutted_phone,
                'fio':{
                    'lastName':self.last_name,
                    'firstName' : self.first_name,
                    'middleName' : self.middle_name,
                },
                'email':self.email
            }
        }

    def to_json(self, method='create'):
        if method == 'create':
            data = {
                'shopId': self.settings.shopId,
                'items' : self.items.to_json(),
                'sum'   : self.items.summ,
                'orderNumber' : self.order_type + '#' + self.order_obj,
            }
            if hasattr(self.settings,'showcaseid'):
                if self.settings.showcaseid is not None:
                    data['showcaseId'] = self.settings.showcaseid

            if self.has_persdata:
                data['values']=self.persdata
            #data['failUrl'] = 'http://mail.ru'
            data['successURL'] = 'http://numerolog.privatebot.info:8080/pay/pay/school/'+self.order_obj
            data['returnURL'] = 'http://numerolog.privatebot.info:8080/pay/pay/school/'+self.order_obj
            data['webhookURL'] = 'http://numerolog.privatebot.info:8080'+reverse('tinkoffWebHookUrl',kwargs={'id':self.id})
            return data
        return {}

class CreditApplicationItemsArray(models.Model):
    application = models.OneToOneField(to=CreditApplication, on_delete=models.CASCADE, verbose_name='Список товаров', related_name='items')
    
    def to_json(self):
        result = []
        for p in self.array.all():
            result.append({
                'name' : p.name,
                'quantity' : p.quantity,
                'price': p.price,
                })
        return result

    @property
    def summ(self):
        summ = Decimal(0) 
        for p in self.array.all():
            summ += p.price
        return summ

class CreditApplicationItemsItem(models.Model):
    array = models.ForeignKey(to=CreditApplicationItemsArray, on_delete=models.CASCADE, verbose_name='Товар',related_name='array')
    name = models.CharField(verbose_name='Название товара', max_length=100,default='')
    quantity = models.PositiveIntegerField(verbose_name='Количество',default=0)
    price = models.DecimalField(verbose_name='Стоимость',max_digits=15,decimal_places=2, default=0)
    category=models.CharField(verbose_name='Категория товара', max_length=100,blank=True)
    vendorCode=models.CharField(verbose_name='Артикул',max_length=100,blank=True)




from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from .consts import TAXES, TAXATIONS
from .settings import get_config
import logging

logging.basicConfig(level='DEBUG')

class Payment(models.Model):
    RESPONSE_FIELDS = {
        'Success': 'success',
        'Status': 'status',
        'PaymentId': 'payment_id',
        'ErrorCode': 'error_code',
        'PaymentURL': 'payment_url',
        'Message': 'message',
        'Details': 'details',
        'Amount' : 'amount',
    }

    amount = models.IntegerField(verbose_name='The amount in cents', editable=False)
###models.CharField(verbose_name='Order number', max_length=100, unique=True, editable=False)
    description = models.TextField(verbose_name='Description', max_length=250, blank=True, default='', editable=False)

    success = models.BooleanField(verbose_name='Successfully completed', default=False, editable=False)
    status = models.CharField(verbose_name='Transaction status', max_length=20, default='', editable=False)
    payment_id = models.CharField(
        verbose_name=_('Unique identifier of the transaction in the Bank system'), max_length=20, default='', editable=False)
    error_code = models.CharField(verbose_name=_('Error code'), max_length=20, default='', editable=False)
    payment_url = models.CharField(
        verbose_name=_('Link to the payment page.'),
        help_text=_('Link to the payment page. By default, the link is available within 24 hours.'),
        max_length=100, blank=True, default='', editable=False)
    message = models.TextField(verbose_name=_('Brief description of the error'), blank=True, default='', editable=False)
    details = models.TextField(verbose_name=_('Detailed description of the error'), blank=True, default='', editable=False)
    terminal = models.ForeignKey('TinkoffSettings', verbose_name="Терминал", blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    order_plural = models.CharField(verbose_name="Название услуги", max_length=100,default='unknw')
    order_obj = models.CharField(verbose_name="Номер услуги", max_length=100, default='unknw')

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    def __unicode__(self):
        return 'Транзакция #{self.id}:{self.payment_id}'.format(self=self)

    def __str__(self):
        return 'Транзакция #{self.id}:{self.order_plural}:{self.order_obj}:{self.status}:{self.success}:{amount}'.format(self=self, amount=self.amount/100)

    def can_redirect(self):
        return self.status == 'NEW' and self.payment_url

    def is_paid(self):
        return self.status == 'CONFIRMED' or self.status == 'AUTHORIZED' or self.status == 'PARTIAL_REFUNDED'

    def is_user_pay(self):
        return self.status == 'CONFIRMED' or self.status == 'AUTHORIZED'

    def is_user_refund(self):
        return self.status == 'PARTIAL_REFUNDED' or self.status == 'REFUNDED'

    def with_receipt(self, email, taxation=None, phone=''):
        if not self.id:
            self.save()

        if hasattr(self, 'receipt'):
            return self

        Receipt.objects.create(payment=self, email=email, phone=phone, taxation=taxation)

        return self

    def with_items(self, items):
        for item in items:
            ReceiptItem.objects.create(receipt=self.receipt, **item)
        return self

    def to_json(self, date_valid=None):
        url_success = settings.SUCCESS_TINKOFF_URL;
        url_fail = settings.FAIL_TINKOFF_URL;
        if self.terminal.using_school:
            url_success += 'school/'
            url_fail += 'school/'
        elif self.terminal.using_services:
            url_success += 'services/'
            url_fail += 'services/'
        else:
            url_success += 'unkwn/'
            url_success += 'unkwn/'


        data = {
            'Amount': self.amount,
            'OrderId': self.id,
            'Description': self.description,
            'NotificationURL' : settings.NOTIFY_TINKOFF_URL,
            'SuccessURL' : url_success+self.order_obj,
            'FailURL' : url_fail+self.order_obj,
        }

        if date_valid is not None:
            data['RedirectDueDate'] = date_valid

        if hasattr(self, 'receipt'):
            data['Receipt'] = self.receipt.to_json()

        return data


class Receipt(models.Model):
    payment = models.OneToOneField(to=Payment, on_delete=models.CASCADE, verbose_name=_('Payment'))
    email = models.CharField(
        verbose_name=_('E-mail address to send the check to the buyer'), max_length=64)
    phone = models.CharField(verbose_name=_('Customer phone'), max_length=64, blank=True, default='')
    taxation = models.CharField(verbose_name=_('Taxation system'), choices=TAXATIONS, max_length=20)

    class Meta:
        verbose_name = _('Check details')
        verbose_name_plural = _('Check data')

    def __unicode__(self):
        return '{} ({})'.format(self.id, self.payment)

    def save(self, *args, **kwargs):
        if not self.taxation:
            self.taxation = get_config()['TAXATION']

        return super(Receipt, self).save(*args, **kwargs)

    def to_json(self):
        return {
            'Email': self.email,
            'Phone': self.phone,
            'Taxation': self.taxation,
            'Items': [item.to_json() for item in self.receiptitem_set.all()]
        }


class ReceiptItem(models.Model):
    receipt = models.ForeignKey(to=Receipt, on_delete=models.CASCADE, verbose_name=_('Check'))
    name = models.CharField(verbose_name=_('Name of goods'), max_length=128)
    price = models.IntegerField(verbose_name=_('Price in cents'))
    quantity = models.DecimalField(verbose_name=_('Quantity/weight'), max_digits=20, decimal_places=3)
    amount = models.IntegerField(verbose_name=_('The amount of cents'))
    tax = models.CharField(verbose_name=_('Tax rate'), max_length=10, choices=TAXES)
    ean13 = models.CharField(verbose_name=_('Barcode'), max_length=20, blank=True, default='')
    shop_code = models.CharField(verbose_name=_('Store code'), max_length=64, blank=True, default='')

    class Meta:
        verbose_name = _('Product information')
        verbose_name_plural = _('Product information')

    def __unicode__(self):
        return '{self.id} (Check {self.receipt.id})'.format(self=self)

    def save(self, *args, **kwargs):
        if not self.amount:
            self.amount = self.price * self.quantity
        if not self.tax:
            self.tax = get_config()['ITEM_TAX']
        return super(ReceiptItem, self).save(*args, **kwargs)

    def to_json(self):
        return {
            'Name': self.name,
            'Price': self.price,
            'Quantity': self.quantity,
            'Amount': self.amount,
            'Tax': self.tax,
            'Ean13': self.ean13,
            'ShopCode': self.shop_code,
        }

class TinkoffSettings(models.Model):
    terminal_id = models.CharField(verbose_name="Номер терминала",max_length=40)
    terminal_key = models.CharField(verbose_name="Пароль терминала", max_length=40)
    using_school = models.BooleanField(verbose_name="Для школы", default = False)
    using_services = models.BooleanField(verbose_name="Для услуг", default = False)
    name = models.CharField(verbose_name="Название терминала",max_length=80,blank=True)

    def __unicode__(self):
        if self.using_school:
            return "Школа"
        elif self.using_services:
            return "Услуги"
        else:
            return "Неизвестный"

    def __str__(self):
        if self.using_school:
            return "Школа " + self.name
        elif self.using_services:
            return "Услуги " + self.name
        else:
            return "Неизвестный " + self.name

    @classmethod
    def get_school_terminal(cls):
        return TinkoffSettings.objects.filter(using_school=True).first()

    @classmethod
    def get_services_terminal(cls):
        return TinkoffSettings.objects.filter(using_services=True).first()


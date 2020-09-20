import django.dispatch
from django_tinkoff_merchant.signals import payment_update
from .tasks import send_app_payment_notify

def payment_check_callback(sender, **kwargs):
    payment = kwargs.get('payment',None)
    amount = kwargs.get('amount',None)
    if payment.apporder_set.count() != 0:
        apporder = payment.apporder_set.first()
        apporder.check_full_payment()
        send_app_payment_notify.delay(apporder.pk,payment.pk, amount)


payment_update.connect(payment_check_callback)

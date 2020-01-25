import django.dispatch
from django_tinkoff_merchant.signals import payment_update


def payment_check_callback(sender, **kwargs):
    payment = kwargs.get('payment',None)
    if payment.schoolappform.count() != 0:
        schoolappform = payment.schoolappform.first()
        schoolappform.check_full_payment()


payment_update.connect(payment_check_callback)

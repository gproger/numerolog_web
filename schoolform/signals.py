import django.dispatch
from django_tinkoff_merchant.signals import payment_update


def payment_check_callback(sender, **kwargs):
    payment = kwargs.get('payment',None)
    if payment.schoolappform_set.count() != 0:
        schoolappform = payment.schoolappform_set.first()
        schoolappform.check_full_payment()


payment_update.connect(payment_check_callback)

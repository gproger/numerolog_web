import django.dispatch
from django_tinkoff_merchant.signals import payment_update
from .tasks import send_school_payment_notify

def payment_check_callback(sender, **kwargs):
    payment = kwargs.get('payment',None)
    amount = kwargs.get('amount',None)
    if payment.schoolappform_set.count() != 0:
        schoolappform = payment.schoolappform_set.first()
        schoolappform.check_full_payment()
        send_school_payment_notify(schoolappform.pk,payment.pk, amount)


payment_update.connect(payment_check_callback)

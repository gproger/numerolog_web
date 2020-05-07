import django.dispatch
from django_tinkoff_merchant.signals import payment_update


def payment_callback(sender, **kwargs):
    payment = kwargs.get('payment',None)
    amount = kwargs.get('amount',None)
    if payment.ticket.count() != 0:
        ticket = payment.ticket.first()
        ticket.check_full_payment()


payment_update.connect(payment_callback)

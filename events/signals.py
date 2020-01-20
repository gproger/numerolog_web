from django_tinkoff_merchant.signals import payment_update
from .models import Ticket

def payment_callback(sender, **kwargs):
    payment = kwargs.get('payment',None)
    if payment.ticket.count() != 0:
        ticket = payment.ticket.first()
        ticket.check_full_payment()


payment_update.connect(payment_callback)

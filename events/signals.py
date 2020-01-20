from django_tinkoff_merchant.signals import payment_update
from .models import Ticket

def payment_callback(sender, **kwargs):
    payment = kwargs.get('payment',None)
    print("Request finished!")
    print(payment)


payment_update.connect(payment_callback)

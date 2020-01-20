from django_tinkoff_merchant.signals import payment_update
from django.dispatch import receiver
from .models import Ticket

@receiver(payment_update)
def payment_callback(sender, **kwargs):
    payment = kwargs.get('payment',None)
    print("Request finished!")
    print(payment)

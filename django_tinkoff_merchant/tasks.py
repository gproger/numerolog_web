from numer.celery import app
from .models import Payment
from .services import MerchantAPI
from django.db.models import Q


@app.task
def update_transactions(arg_test):
    payments = Payment.objects.filter(Q(status='NEW') | Q(status='FORM_SHOWED'))
    for p in payments: 
        MerchantAPI().status(p)
        p.save()
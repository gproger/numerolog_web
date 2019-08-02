from django.db import models

# Create your models here.


class Payment(models.Model):
    TINKOFF = 'tin'
    ROBOKASSA = 'rob'
    MERCH = [
        (TINKOFF, 'Tinkoff'),
        (ROBOKASSA, 'Robokassa'),
    ]
    merch = models.CharField(max_length=3, choices=MERCH, default=ROBOKASSA)
    app = models.ForeignKey('AppOrder', on_delete=models.DO_NOTHING,
                            related_name='payment',
                            related_query_name='payment')
    amount = models.DecimalField(max_digits=8, decimal_placed=2)
    currency = models.CharField(max_length=5, default='RUB')
    

from django.contrib import admin

from .models import *
admin.site.register(TinkoffCreditSettings)
admin.site.register(CreditApplication)
admin.site.register(CreditApplicationItemsArray)
admin.site.register(CreditApplicationItemsItem)
# Register your models here.

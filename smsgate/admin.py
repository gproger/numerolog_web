from django.contrib import admin
from .models import SMSSettings
from .models import SendedSMS
# Register your models here.

admin.site.register(SMSSettings)
admin.site.register(SendedSMS)

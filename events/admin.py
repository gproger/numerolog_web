from django.contrib import admin
from .models import *

admin.site.register(OfflineEvent)
admin.site.register(EventTicketTemplate)
admin.site.register(Ticket)

# Register your models here.

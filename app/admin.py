from django.contrib import admin
from .models import AppOrder
from .models import AppResultFile

admin.site.register(AppOrder)
admin.site.register(AppResultFile)

# Register your models here.

from django.contrib import admin
from .models import AppUser, AppOrder

admin.site.register(AppUser)
admin.site.register(AppOrder)

# Register your models here.

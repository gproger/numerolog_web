from django.contrib import admin
from .models import AppOrder
from .models import AppResultFile
from .models import AppAutoGeneratorOptions

admin.site.register(AppOrder)
admin.site.register(AppResultFile)
admin.site.register(AppAutoGeneratorOptions)

# Register your models here.

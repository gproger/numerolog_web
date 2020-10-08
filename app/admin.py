from django.contrib import admin
from .models import AppOrder
from .models import AppResultFile
from .models import AppAutoGeneratorOptions
from .models import AppExpertUser

admin.site.register(AppOrder)
admin.site.register(AppResultFile)
admin.site.register(AppAutoGeneratorOptions)
admin.site.register(AppExpertUser)

# Register your models here.

from django.contrib import admin
from .models import SchoolAppForm, SchoolAppFlow, SchoolAppWorker

admin.site.register(SchoolAppForm)
admin.site.register(SchoolAppFlow)
admin.site.register(SchoolAppWorker)


# Register your models here.

from django.contrib import admin
from .models import SchoolAppForm, SchoolAppFlow, SchoolAppCurator

admin.site.register(SchoolAppForm)
admin.site.register(SchoolAppFlow)

def flow_name(obj):
    return obj.flow.flow_name

@admin.register(SchoolAppCurator)
class SchoolAppCuratorAdmin(admin.ModelAdmin):
    list_display = ['id', 'email','phone','first_name',
        'middle_name', 'last_name','instagramm','bid',flow_name,'curator','expert']
    search_fields = ['phone','email','first_name','last_name','middle_name']
    list_filter = ['curator','expert','flow__flow_name']




# Register your models here.

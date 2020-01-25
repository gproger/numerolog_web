from django.contrib import admin
from .models import SchoolAppForm, SchoolAppFlow, SchoolAppCurator

admin.site.register(SchoolAppForm)

def flow_name(obj):
    return obj.flow.flow_name

@admin.register(SchoolAppCurator)
class SchoolAppCuratorAdmin(admin.ModelAdmin):
    list_display = ['id', 'email','phone','first_name',
        'middle_name', 'last_name','instagramm','bid',flow_name,'curator','expert']
    search_fields = ['phone','email','first_name','last_name','middle_name']
    list_filter = ['curator','expert','flow__flow_name']


def registered(obj):
    return obj.schoolappform_set.count

def curators(obj):
    return obj.schoolappcurator_set.count

@admin.register(SchoolAppFlow)
class SchoolAppFlowAdmin(admin.ModelAdmin):
    list_display = ['id','flow','flow_name','state','price',registered, curators]



# Register your models here.

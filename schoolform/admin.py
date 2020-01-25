from django.contrib import admin
from django.db.models import F
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
    return obj.schoolappform_set.count()

def pre_pay(obj):
    return obj.schoolappform_set.filter(payed_amount__gt=0).filter(payed_amount__lt=F('price')).count()

def full_pay(obj):
    return obj.schoolappform_set.filter(payed_amount=F('price')).count()

def no_pay(obj):
    return obj.schoolappform_set.filter(payed_amount=0).count()

def curators(obj):
    return obj.schoolappcurator_set.count()

registered.short_description = 'Всего'
pre_pay.short_description = 'С предоплатой'
full_pay.short_description = 'Оплачено'
no_pay.short_description = 'Без оплаты'
curators.short_description = 'Кураторов'

@admin.register(SchoolAppFlow)
class SchoolAppFlowAdmin(admin.ModelAdmin):
    list_display = ['id','flow','flow_name','state','price',registered, no_pay,pre_pay, full_pay,curators]
    list_filter = ['state']


# Register your models here.

from django.contrib import admin
from django.db.models import F, Q
from django_tinkoff_merchant.services import MerchantAPI
from .models import SchoolAppForm, SchoolAppFlow, SchoolAppCurator, SchoolAppPersCuratorForm
from schoolform.tasks import send_school_form_pay_url

def flow_name(obj):
    return obj.flow.flow_name

admin.site.register(SchoolAppPersCuratorForm)

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

def payed(obj):
    value = 'Да'
    if obj.payed_amount != obj.price:
        value='Нет'
    return value

payed.short_description = 'Полностью оплачено'

class PayedListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Полностью оплачено'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'payed'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            (None, 'Неважно'),
            (True, 'Да'),
            (False, 'Нет'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() is None:
            return queryset

        if self.value():
            return queryset.filter(payed_amount=F('price'))
        else:
            return queryset.filter(~Q(payed_amount=F('price')))



def resend_payment_url(modeladmin, request, qs):
    for p in qs:
        send_school_form_pay_url.delay(p.pk)

def refund_payments(modeladmin, request, qs):
    for p in qs:
        for paym in p.payment.all():
            MerchantAPI().cancel(paym)
            paym.save()

def status_payments(modeladmin, request, qs):
    for p in qs:
        for paym in p.payment.all():
            if paym.status != 'CONFIRMED':
                MerchantAPI().status(paym)
                paym.save()


def recalc_payments(modeladmin, request, qs):
    for p in qs:
        p.check_full_payment()


resend_payment_url.short_description = 'Выслать письмо для оплаты'
refund_payments.short_description = 'Отменить платеж(и)'
status_payments.short_description = 'Проверить платеж(и)'
recalc_payments.short_description = 'Перепроверить оплату'


@admin.register(SchoolAppForm)
class SchoolAppFormAdmin(admin.ModelAdmin):
    list_display = ['id', 'email','phone','first_name',
        'middle_name', 'last_name','instagramm','bid',flow_name,'pay_url_sended','payed_amount','price',payed]
    list_filter = ['flow__flow_name',PayedListFilter]
    actions = [ resend_payment_url, status_payments, recalc_payments, refund_payments]
    search_fields = ['id', 'phone','email','first_name','middle_name','last_name']


# Register your models here.

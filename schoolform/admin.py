from django.contrib import admin
from django.db.models import F, Q
from django_tinkoff_merchant.services import MerchantAPI
from .models import SchoolAppForm, SchoolAppFlow, SchoolAppCurator, SchoolAppPersCuratorForm
from schoolform.tasks import send_school_form_pay_url, send_school_from_pay_notify
from schoolform.tasks import send_pay_notify_sms
from django.shortcuts import render
from .forms import RefundForm

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
            (True, 'Да'),
            (False, 'Нет'),
            ('NotFull', 'Не полная оплата')
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

        if self.value() == 'True':
            return queryset.filter(payed_amount=F('price'))
        elif self.value() == 'False':
            return queryset.filter(~Q(payed_amount=F('price')))
        elif self.value() == 'NotFull':
            return queryset.filter(~Q(payed_amount=F('price'))).filter(payed_amount__gt=0)



def resend_payment_url(modeladmin, request, qs):
    for p in qs:
        send_school_form_pay_url.delay(p.pk)

def cancel_payments(modeladmin, request, qs):
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


def send_pay_notify_url(modeladmin, request, qs):
    for p in qs:
        send_school_from_pay_notify.delay(p.pk)

def admin_send_pay_notify_sms(modeladmin, request, qs):
    for p in qs:
        send_pay_notify_sms.delay(p.pk)

def refund_payments(modeladmin, request, queryset):
    form = None

    if 'apply' in request.POST:
        form = RefundForm(request.POST)

        if form.is_valid():
            amount = form.cleaned_data['amount']
            is_percent = form.cleaned_data['is_percent']

            count = 0
            for item in queryset:
                total_amount = 0
                for p in item.payment.all():
                    if p.is_paid():
                        total_amount += p.amount

                ret_amount = amount
                if is_percent:
                    ret_amount = total_amount * (100-amount)/100
                else:
                    ret_amount = ret_amount * 100

                count = ret_amount

            modeladmin.message_user(request, "Возврат на сумму %d " % (count))
            return HttpResponseRedirect(request.get_full_path())

    if not form:
        form = RefundForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

    return render(request, 'schoolform/refund.html', {'items': queryset,'form': form, 'title':u'Возврат платежа(ей)'})



resend_payment_url.short_description = 'Выслать письмо для оплаты'
send_pay_notify_url.short_description = 'Выслать Напоминание о оплате'
status_payments.short_description = 'Проверить платеж(и)'
recalc_payments.short_description = 'Перепроверить оплату'
admin_send_pay_notify_sms.short_description = 'Выслать SMS Напоминание о оплате'
refund_payments.short_description = 'Сделать возврат(ы)'


@admin.register(SchoolAppForm)
class SchoolAppFormAdmin(admin.ModelAdmin):
    list_display = ['id', 'email','phone','first_name',
        'middle_name', 'last_name','instagramm','bid',flow_name,'pay_url_sended','payed_amount','price',payed]
    list_filter = ['flow__flow_name',PayedListFilter]
    actions = [ resend_payment_url, send_pay_notify_url, admin_send_pay_notify_sms, status_payments, recalc_payments, refund_payments]
    search_fields = ['id', 'phone','email','first_name','middle_name','last_name']


# Register your models here.

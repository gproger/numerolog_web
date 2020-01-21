from django.contrib import admin
from .models import *
from django_tinkoff_merchant.services import MerchantAPI

admin.site.register(OfflineEvent)
admin.site.register(EventTicketTemplate)

def resend_ticket(modeladmin, request, qs):
    for p in qs:
        p.send_ticket_to_email()

def resend_payment_url(modeladmin, request, qs):
    for p in qs:
        p.send_new_ticket_payurl()

def refund_payments(modeladmin, request, qs):
    for p in qs:
        for paym in p.payment:
            MerchantAPI.cancel(paym)
            paym.save()


resend_payment_url.short_description = 'Выслать письмо для оплаты'
resend_ticket.short_description = 'Выслать билет'
refund_payments.short_description = 'Отменить платеж(и)'

@admin.register(Payment)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_amount_rub', 'phone','email','first_name',
        'middle_name', 'last_name']
    list_filter = ['status', 'success']
    search_fields = ['id', 'phone','email']
    actions = [resend_payment_url,resend_ticket,refund_payments]

    def get_amount_rub(self, obj):
        return obj.get_amount()/100

    get_amount_rub.short_description = 'Сумма (руб)'


# Register your models here.

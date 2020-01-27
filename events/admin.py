from django.contrib import admin
from .models import *
from django_tinkoff_merchant.services import MerchantAPI
from events.tasks import send_new_ticket_payurl, send_ticket_to_email

admin.site.register(OfflineEvent)
admin.site.register(EventTicketTemplate)

def resend_ticket(modeladmin, request, qs):
    for p in qs:
        send_ticket_to_email.delay(p.pk)

def resend_payment_url(modeladmin, request, qs):
    for p in qs:
        send_new_ticket_payurl.delay(p.pk)

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


resend_payment_url.short_description = 'Выслать письмо для оплаты'
resend_ticket.short_description = 'Выслать билет'
refund_payments.short_description = 'Отменить платеж(и)'
status_payments.short_description = 'Проверить платеж(и)'

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'price','get_amount_rub', 'phone','email','first_name',
        'middle_name', 'last_name','ticket_sended','pay_url_sended']
    search_fields = ['id', 'phone','email','first_name','middle_name','last_name']
    list_filter = ['price','ticket_sended','pay_url_sended']
    actions = [resend_payment_url,resend_ticket,status_payments,refund_payments]

    def get_amount_rub(self, obj):
        return obj.get_amount(obj)

    get_amount_rub.short_description = 'Сумма (руб)'


# Register your models here.

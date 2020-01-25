import django.dispatch
from django_tinkoff_merchant.signals import payment_update
from events.tasks import send_new_ticket_payurl, send_ticket_to_email

send_ticket_pdf = django.dispatch.Signal(providing_args=['tick_id'])
send_ticket_pay_email = django.dispatch.Signal(providing_args=['tick_id'])

def payment_callback(sender, **kwargs):
    payment = kwargs.get('payment',None)
    if payment.ticket.count() != 0:
        ticket = payment.ticket.first()
        ticket.check_full_payment()


def send_ticket_pdf_callback(sender, **kwargs):
    tick_id = kwargs.get('tick_id',None)
    send_ticket_to_email.delay(tick_id, retry_jitter=True,ignore_result=True)


def send_ticket_pay_email_callback(sender, **kwargs):
    tick_id = kwargs.get('tick_id',None)
    send_new_ticket_payurl.delay(tick_id, retry_jitter=True,ignore_result=True)

payment_update.connect(payment_callback)
send_ticket_pdf.connect(send_ticket_pdf_callback)
send_ticket_pay_email.connect(send_ticket_pay_email_callback)

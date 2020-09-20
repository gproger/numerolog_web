
from emails.emails import mail_user
from django.template.loader import render_to_string
from django.template import Template
from django.template import Context

from numer.celery import app
from django.conf import settings
from app.models import AppOrder

DEFAULT_SENDER = 'neNumerolog'

@app.task
def send_create_notifications(app_id):
    app = AppOrder.objects.get(pk=app_id)

    context = {
        'url_pay' : settings.MISAGO_ADDRESS+'/pay/pay/school/'+str(form.id),
        'user_name' : app.first_name + ' ' + app.last_name,
        "SITE_HOST" : settings.MISAGO_ADDRESS,
    }
    mail_user(form, "Школа неНумерологии",'emails/create_school_form',
        context=context, sender=DEFAULT_SENDER)



@app.task
def send_create_notifications(app_id):
    app = AppOrder.objects.get(pk=app_id)

    context = {
        'user_name' : app.first_name + ' ' + app.last_name,
        'user_status' : current_status,
        "SITE_HOST" : settings.MISAGO_ADDRESS,
    }
    mail_user(form, "Школа неНумерологии",'emails/expert_school_form',
        context=context, sender=DEFAULT_SENDER)


@app.task
def send_app_payment_notify(form_id, payment_id,amount):
    form = AppOrder.objects.get(pk=form_id)
    payment = form.payment.get(pk=payment_id)

    context = {
        'url_pay' : settings.MISAGO_ADDRESS+'/profile/orders.',
        'user_name' : form.first_name + ' ' + form.last_name,
        'order_num' : form.id,
        'price' : form.price,
        'total_amount' : form.payed_amount,
        'amount' : amount//100,
        'trans' : payment.status,
        "SITE_HOST" : settings.MISAGO_ADDRESS,
    }

    if payment.success:
        if payment.is_user_pay():
            mail_user(form, "Школа неНумерологии",'emails/notify_order_payment_accepted_mail',
                context=context, sender=DEFAULT_SENDER)
        elif payment.is_user_refund():
            mail_user(form, "Школа неНумерологии",'emails/notify_apporder_payment_refunded_mail',
                context=context, sender=DEFAULT_SENDER)


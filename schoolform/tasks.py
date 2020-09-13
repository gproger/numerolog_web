
from emails.emails import mail_user
from django.template.loader import render_to_string
from django.template import Template
from django.template import Context
from weasyprint import HTML

from numer.celery import app
from django.conf import settings
from schoolform.models import SchoolAppForm, SchoolAppCurator
from smsgate.services import SendSMSAPI

DEFAULT_SENDER = 'neNumerolog'

@app.task
def send_school_form_pay_url(form_id):
    form = SchoolAppForm.objects.get(pk=form_id)

    context = {
        'url_pay' : settings.MISAGO_ADDRESS+'/pay/pay/school/'+str(form.id),
        'user_name' : form.first_name + ' ' + form.last_name,
        "SITE_HOST" : settings.MISAGO_ADDRESS,
    }
    mail_user(form, "Школа неНумерологии",'emails/create_school_form',
        context=context, sender=DEFAULT_SENDER)
    form.pay_url_sended = True
    form.save()

@app.task
def send_school_curator_registered(form_id):
    form = SchoolAppCurator.objects.get(pk=form_id)
    current_status = ''
    if form.curator:
        if form.expert:
            current_status = 'экспертом и куратором'
        else:
            current_status = 'куратором'
    elif form.expert:
        current_status = 'экспертом'

    context = {
        'user_name' : form.first_name + ' ' + form.last_name,
        'user_status' : current_status,
        "SITE_HOST" : settings.MISAGO_ADDRESS,
    }
    mail_user(form, "Школа неНумерологии",'emails/expert_school_form',
        context=context, sender=DEFAULT_SENDER)

@app.task
def send_school_from_pay_notify(form_id):
    form = SchoolAppForm.objects.get(pk=form_id)

    context = {
        'url_pay' : settings.MISAGO_ADDRESS+'/pay/pay/school/'+str(form.id),
        'user_name' : form.first_name + ' ' + form.last_name,
        'flow_num' : form.flow.flow,
        'flow_name' : form.flow.flow_name,
        'recr_end' : form.flow.recruitment_stop,
        'price' : form.price,
        'amount' : form.payed_amount,
        "SITE_HOST" : settings.MISAGO_ADDRESS,
    }

    mail_user(form, "Школа неНумерологии",'emails/notify_pay_mail',
        context=context, sender=DEFAULT_SENDER)

@app.task
def send_pay_notify_sms(form_id):
    form = SchoolAppForm.objects.get(pk=form_id)
    context = {
        'url_pay' : settings.MISAGO_ADDRESS+'/pay/pay/school/'+str(form.id),
        'recr_end' : form.flow.recruitment_stop,
    }

    sms = SendSMSAPI()
    sms.send_pay_notify_smd(form.phone, context)


@app.task
def send_school_payment_notify(form_id, payment_id,amount):
    form = SchoolAppForm.objects.get(pk=form_id)
    payment = form.payment.get(pk=payment_id)

    context = {
        'url_pay' : settings.MISAGO_ADDRESS+'/pay/pay/school/'+str(form.id),
        'user_name' : form.first_name + ' ' + form.last_name,
        'flow_num' : form.flow.flow,
        'flow_name' : form.flow.flow_name,
        'recr_end' : form.flow.education_start,
        'price' : form.price,
        'total_amount' : form.payed_amount,
        'amount' : amount//100,
        'trans' : payment.status,
        "SITE_HOST" : settings.MISAGO_ADDRESS,
    }

    if payment.success:
        if payment.is_user_pay():
            mail_user(form, "Школа неНумерологии",'emails/notify_payment_accepted_mail',
                context=context, sender=DEFAULT_SENDER)
        elif payment.is_user_refund():
            mail_user(form, "Школа неНумерологии",'emails/notify_payment_refunded_mail',
                context=context, sender=DEFAULT_SENDER)


@app.task
def send_payed_notify_task(form_id):
    form = SchoolAppForm.objects.get(pk=form_id)

    context = {
        'user_name' : form.first_name + ' ' + form.last_name,
        'flow_num' : form.flow.flow,
        'flow_name' : form.flow.flow_name,
        'price' : form.price,
        'total_amount' : form.payed_amount,
        "SITE_HOST" : settings.MISAGO_ADDRESS,
    }

    if context['price'] == context['total_amount']:
        mail_user(form, "Школа неНумерологии",'emails/notify_payment_all_mail',
                context=context, sender=DEFAULT_SENDER)


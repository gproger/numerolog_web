
from emails.emails import mail_user
from django.template.loader import render_to_string
from django.template import Template
from django.template import Context
from weasyprint import HTML

from numer.celery import app
from django.conf import settings
from schoolform.models import SchoolAppForm, SchoolAppCurator

@app.task
def send_school_form_pay_url(form_id):
    form = SchoolAppForm.objects.get(pk=form_id)

    context = {
        'url_pay' : settings.MISAGO_ADDRESS+'/pay/pay/school/'+str(form.id),
        'user_name' : form.first_name + ' ' + form.last_name,
        "SITE_HOST" : settings.MISAGO_ADDRESS,
    }
    mail_user(form, "Школа неНумерологии",'emails/create_school_form',context=context)
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
    mail_user(form, "Школа неНумерологии",'emails/expert_school_form',context=context)
    

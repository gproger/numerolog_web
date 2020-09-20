
from emails.emails import mail_user
from django.template.loader import render_to_string
from django.template import Template
from django.template import Context

from numer.celery import app
from django.conf import settings
from app.models import AppOrder
from app.models import AppAutoGeneratorOptions
from app.models import AppResultFile
import requests,re
from bs4 import BeautifulSoup
import uuid
import time
import tempfile

DEFAULT_SENDER = 'neNumerolog'

@app.task
def send_create_notifications(app_id):
    app = AppOrder.objects.get(id=app_id)

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
    form = AppOrder.objects.get(id=form_id)
    payment = form.payment.get(id=payment_id)

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


@app.task
def get_automatic_description(order_id,bid):
    settings = AppAutoGeneratorOptions.objects.first()
    session = requests.session()
    r1 = session.get(settings.url_login)
    bsoup = BeautifulSoup(r1.content,'html.parser')
    login_data={'username':settings.username,'password':settings.userpass,'csrfmiddlewaretoken':bsoup.input['value'],\
        'next':'/calc/downAPIDesc/?template='+str(settings.templateid)+'&bid='+bid}
    r2 = session.post(settings.url_login,data=login_data)
    with tempfile.NamedTemporaryFile(delete=True) as tFile:
        tFile.write(r2.content)
        appOrder = AppOrder.objects.get(id=order_id)
        if appOrder is None:
            return
        appFileResult = AppResultFile()
        appFileResult.order=appOrder
        appFileResult.title='Автоматическое описание'
        appFileResult.file.save(str(int(round(time.time() * 1000)))+'-'+str(uuid.uuid4())+'.pdf',tFile)
        appFileResult.save()
    return 0


@app.task
def appResultFileAdded(app_id):
    file = AppResultFile.objects.get(pk=app_id)
    form = file.order
    
    context = {
        'url_pay' : settings.MISAGO_ADDRESS+'/service/'+str(form.id),
        'user_name' : form.first_name + ' ' + form.last_name,
        'order_num' : form.id,
        'title'     : file.title,
        "SITE_HOST" : settings.MISAGO_ADDRESS,
    }

    mail_user(form, "Школа неНумерологии",'emails/notify_apporder_payment_file_added',
                context=context, sender=DEFAULT_SENDER)

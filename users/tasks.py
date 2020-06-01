
from emails.emails import mail_user
from django.template.loader import render_to_string
from django.template import Template
from django.template import Context
from weasyprint import HTML

from numer.celery import app
from django.conf import settings
from users.models import UserInfo
import random


DEFAULT_SENDER = 'neNumerolog'

@app.task
def send_email_code(userInfo_id):
    userInfo = UserInfo.objects.get(pk=userInfo_id)
    userInfo.email_validation_code = random.randrange(100000,1000000,1)

    context = {
        "SITE_HOST" : settings.MISAGO_ADDRESS,
        "code" : userInfo.email_validation_code,
    }
    userInfo.save()

    receipent = lambda: None
    receipent.email = userInfo.email_temp

    mail_user(receipent, "Школа неНумерологии",'emails/validate_email_form',
        context=context, sender=DEFAULT_SENDER)


@app.task
def send_email_passwd(userInfo_id, passwd):
    userInfo = UserInfo.objects.get(pk=userInfo_id)

    context = {
        "SITE_HOST" : settings.MISAGO_ADDRESS,
        "passwd" : passwd,
    }

    receipent = lambda: None
    receipent.email = userInfo.email

    mail_user(receipent, "Школа неНумерологии",'emails/new_user_email_passwd',
        context=context, sender=DEFAULT_SENDER)

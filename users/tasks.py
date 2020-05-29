
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
def send_email_code(form_id):
    userInfo = UserInfo.objects.get(pk=form_id)
    userInfo.code = random.randrange(100000,1000000,1)

    context = {
        "SITE_HOST" : settings.MISAGO_ADDRESS,
        "code" : userInfo.code,
    }
    userInfo.save()

    receipent = {}
    receipent.email = userInfo.email_temp

    mail_user(receipent, "Школа неНумерологии",'emails/validate_email_form',
        context=context, sender=DEFAULT_SENDER)


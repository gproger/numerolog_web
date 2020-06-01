from django.core import mail as djmail
from django.template.loader import render_to_string
from django.utils.translation import get_language

#from ..conf import settings
#from .utils import get_host_from_address


def build_mail(recipient, subject, template, sender=None, context=None, attach=None):
    context = context.copy() if context else {}

    context.update(
        {
            "LANGUAGE_CODE": 'ru',
#            "LOGIN_URL": settings.LOGIN_URL,
#            "forum_host": get_host_from_address(forum_address),
            "email" : recipient.email,
            "user": recipient,
            "sender": sender,
            "subject": subject,
        }
    )

    message_plain = render_to_string("%s.txt" % template, context)
    message_html = render_to_string("%s.html" % template, context)

    message = djmail.EmailMultiAlternatives(
        subject, message_plain, to=[recipient.email]
    )
    message.attach_alternative(message_html, "text/html")
    if attach is not None:
        for k in attach:
            message.attach(k['filename'],k['file'])

    return message


def mail_user(recipient, subject, template, sender=None, context=None, attach=None):
    message = build_mail(recipient, subject, template, sender, context, attach)
    message.send()


def mail_users(recipients, subject, template, sender=None, context=None):
    messages = []

    for recipient in recipients:
        messages.append(build_mail(recipient, subject, template, sender, context))

    if messages:
        send_messages(messages)


def send_messages(messages):
    connection = djmail.get_connection()
    connection.send_messages(messages)

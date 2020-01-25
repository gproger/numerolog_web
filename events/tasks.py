
from emails.emails import mail_user
from django.template.loader import render_to_string
from django.template import Template
from django.template import Context
from weasyprint import HTML
#from events.models import Ticket

from myproject.celery import app
from django.conf import settings


@app.task
def send_new_ticket_payurl(ticket_id):
    ticket = Ticket.object.get(pk=ticket_id)
    context = {
        'url_pay' : settings.MISAGO_ADDRESS+'/pay/pay/ticket/'+str(ticket.id),
        'user_name' : ticket.first_name + ' ' + ticket.last_name,
        "SITE_HOST" : settings.MISAGO_ADDRESS,
    }
#        attach = []
#        ticket = {
#        'filename' : 'ticket.pdf',
#        'file' : None
#        }
#        attach.append(ticket)
    mail_user(self, "Оплата и проверка оплаты встречи с Ольгой Перцевой",'emails/ticket',context=context)


@app.task
def send_ticket_to_email(ticket_id):
    ticket = Ticket.object.get(pk=ticket_id)
    templ = Template(ticket.eventticket.template)
    tick = {
     'id' : ticket.id,
     'name' : ticket.eventticket.event.name,
     'place' : ticket.eventticket.event.address,
     'first_name' : ticket.first_name,
     'middle_name' : ticket.middle_name,
     'last_name' : ticket.last_name,
     'price' : ticket.price,
    }
    cont = Context({ 'ticket' : tick} )


    html = templ.render(cont)

    html = HTML(string=html)
    result = html.write_pdf()

    context = {
        'user_name' : ticket.first_name + ' ' + ticket.last_name,
        "SITE_HOST" : settings.MISAGO_ADDRESS,
    }
    attach = []
    ticket = {
    'filename' : 'ticket.pdf',
    'file' : result
    }
    attach.append(ticket)
    mail_user(self, "Билет на встречу с Ольгой Перцевой",'emails/ticket_ok',context=context, attach=attach)

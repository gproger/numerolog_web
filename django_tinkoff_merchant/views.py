from __future__ import unicode_literals

import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt

from .models import Payment
from .services import MerchantAPI
from .signals import payment_update
import logging
logging.basicConfig(level='DEBUG')


logging.info("Tinkoff views.py")

class Notification(View):
    _merchant_api = None

    @property
    def merchant_api(self):
        if not self._merchant_api:
            self._merchant_api = MerchantAPI()
        return self._merchant_api

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        logging.info(request)
        logging.info(request.method)
        return super(Notification, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logging.info("post method called")
        data = json.loads(request.body.decode())


        logging.info("Tinkoff post available")

        payment = get_object_or_404(Payment, payment_id=data.get('PaymentId'))

        logging.info("Payment available")

        if data.get('TerminalKey') != payment.terminal.terminal_id:
            logging.info('Bad terminal key')
            return HttpResponse(b'Bad terminal key', status=400)


        if not self.merchant_api.token_correct(data.get('Token'), data, payment.terminal):
            logging.info('Bad token')
            return HttpResponse(b'Bad token', status=400)


        self.merchant_api.update_payment_from_response(payment, data).save()

        logging.info('SAVED')

        payment_update.send(self.__class__, payment=payment)

        return HttpResponse(b'OK', status=200)

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



class SmsNotify(View):
    pass

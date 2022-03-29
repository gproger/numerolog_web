from __future__ import unicode_literals

import json
from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt

import logging


class Notification(View):
    def post(self,request, *args, **kwargs):
        data = json.loads(request.body.decode())
        print("received nottifaction from tcb")
        print(data)
        return HttpResponse(b'OK', status=200)

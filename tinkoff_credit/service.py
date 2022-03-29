from .models import *

from .consts import *
import requests
import json
from .utils import Encoder


class TinkoffCreditHTTPException(Exception):
    pass

RESP_ARRAY = {
   'id': 'tcb_id',
   'link' : 'link_url',
}

class TinkoffCreditAPI(object):


    def update_crapp(self, obj, response):
        for k in response:
            setattr(obj,RESP_ARRAY[k],response.get(k))
        obj.save()
#            print("key " + k + " val " + response.get(k))

    def _request(self, url, method, obj):
        url = URLS[url]
        if not url.startswith("CREATE"):
            url = url.format(obj.id)
        
        request = method(url, data=json.dumps(obj.to_json(), cls=Encoder), headers={'Content-Type': 'application/json'})
        print(request)
        if request.status_code != 200:
            raise TinkoffCreditHTTPException('bad status code')
        print(request)
        return request


    def createDemo(self, crapp):
        response = self._request('CREATE_DEMO', requests.post, crapp).json()
        return self.update_crapp(crapp, response)

    def create(self, crapp):
        response = self._request('CREATE', requests.post, crapp).json()
        return self.update_crapp(crapp, response)

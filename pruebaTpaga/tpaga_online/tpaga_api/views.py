# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from urllib import parse as urlparse
import requests


# Create your views here.
from rest_framework import generics

TPAGA_PRIVATE_TOKEN = 'd13fr8n7vhvkuch3lq2ds5qhjnd2pdd2'
TPAGA_API_URL = 'https://sandbox.tpaga.co/api/customer'


class TpagaTestClient(generics.GenericAPIView):
    def __init__(
            self,
            private_token=TPAGA_PRIVATE_TOKEN,
            base_url=TPAGA_API_URL,
    ):
        self.base_url = base_url
        self.private_token = private_token

    # ******************************************
    # saludo = "Buenos Días"
    #
    # def get(self, request):
    #      return HttpResponse(self.saludo)
    # ******************************************

    def api_post(self, path, data, token=None):
        if not token:
            token = self.private_token
        return requests.post(
            urlparse.urljoin(self.base_url, path),
            json=data, auth=(token, ''),
        )

    def fail(self, response):
        raise Exception(
            'Whoops, got\n\nSTATUS: {}\n\nHEADERS: {}\n\nCONTENT: {}'.format(
                response.status_code,
                response.headers,
                response.content,
            ))

    def json_from_response(self, response, expected_http_code=None):
        if not expected_http_code:
            expected_http_code = [201]
        if response.status_code not in expected_http_code:
            self.fail(response)
        if not response.content:
            return None
        return response.json()

    def create_customer(self, data):
        response = self.api_post('customer', data)
        return self.json_from_response(response)

    def assoc_cc_to_customer(self, customer_token, cc_temp_token=None):
        cdata = {'token': cc_temp_token}
        response = self.api_post('customer/{}/credit_card_token'.format(customer_token), cdata)
        return self.json_from_response(response)

    def charge_cc(self, cc_token, order_id='BGR-2', amount=1000):
        cdata = {
            'orderId': order_id,
            'currency': 'COP',
            'taxAmount': 0,
            'description': 'One bridge in god condition',
            'installments': 1,
            'amount': amount,
            'crediCard': cc_token,
        }
        response = self.api_post('charge/credit_card', cdata)
        return self.jason_from_response(response)

    def refund_cc(self, cc_charge_id):
        cdata = {
            'id': cc_charge_id,
        }
        response = self.api_post('refund/credit_card', cdata)
        return self.json_from_response(response, expected_http_code=[202])
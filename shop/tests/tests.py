from django.test import TestCase
from shop import woocommerce
from shop.tests import mocks
import json
from httmock import all_requests, HTTMock, response


def mock_response(status_code, content, request, headers={}):
    return response(status_code, content, headers, None, 5, request)


@all_requests
def response_mock(url, request):
    if request.method == 'GET':
        if 'customers/' in url.path:
            return mock_response(200, json.dumps(mocks.CUSTOMER_RESPONSE), request)
        elif 'customers' in url.path:
            return mock_response(200, json.dumps(mocks.ALL_CUSTOMERS_RESPONSE), request)
    elif request.method == 'POST':
        return mock_response(201, json.dumps(mocks.CUSTOMER_RESPONSE), request)
    elif request.method == 'PUT':
        return mock_response(200, json.dumps(mocks.CUSTOMER_RESPONSE), request)
    elif request.method == 'DELETE':
        return mock_response(200, json.dumps(mocks.CUSTOMER_RESPONSE), request)


class CustomerTests(TestCase):
    @all_requests
    def test_get_all_customers(self):
        with HTTMock(response_mock):
            resp = woocommerce.get_all_customers()
            self.assertListEqual(resp, mocks.ALL_CUSTOMERS_RESPONSE)

    @all_requests
    def test_get_customer(self):
        with HTTMock(response_mock):
            resp = woocommerce.get_customer(25)
            self.assertDictEqual(resp, mocks.CUSTOMER_RESPONSE)

    @all_requests
    def create_customer(self):
        with HTTMock(response_mock):
            resp = woocommerce.create_customer(mocks.CUSTOMER_RESPONSE)
            self.assertDictEqual(resp, mocks.CUSTOMER_RESPONSE)

    @all_requests
    def update_customer(self):
        with HTTMock(response_mock):
            resp = woocommerce.update_customer(mocks.UPDATE_CUSTOMER_DATA, 25)
            self.assertDictEqual(resp, mocks.CUSTOMER_RESPONSE)

    @all_requests
    def delete_customer(self):
        with HTTMock(response_mock):
            resp = woocommerce.delete_customer(25)
            self.assertDictEqual(resp, mocks.CUSTOMER_RESPONSE)


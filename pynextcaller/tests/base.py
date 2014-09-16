# -*- coding: utf-8 -*-
import unittest
try:
    from unittest import mock
except ImportError:
    import mock
from pynextcaller.client import Client
from pynextcaller import transport


class BaseTestCase(unittest.TestCase):

    class FakeResponse(object):
        pass

    def __init__(self, *args, **kwargs):
        super(BaseTestCase, self).__init__(*args, **kwargs)
        self.client = None
        self.fake_response = None
        self.request_patcher = None

    def patch_http_request(self, result):
        self.mock.return_value = result

    def setUp(self):
        api_key = 'api_key'
        api_secret = 'api_secret'
        self.api_request = transport.api_request
        self.mock = mock.Mock()
        transport.api_request = self.mock
        self.client = Client(api_key, api_secret)
        self.fake_response = self.FakeResponse()
        self.fake_response.status_code = 204

    def tearDown(self):
        transport.api_request = self.api_request

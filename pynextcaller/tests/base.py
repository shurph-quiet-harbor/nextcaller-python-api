# -*- coding: utf-8 -*-
from mocker import MockerTestCase
from pynextcaller.client import Client


class BaseTestCase(MockerTestCase):

    class FakeResponse(object):
        pass

    def __init__(self, *args, **kwargs):
        super(BaseTestCase, self).__init__(*args, **kwargs)
        self.client = None
        self.fake_response = None

    def setUp(self):
        api_key = 'api_key'
        api_secret = 'api_secret'
        self.client = Client(api_key, api_secret)
        self.fake_response = self.FakeResponse()
        self.fake_response.status_code = 204

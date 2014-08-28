# -*- coding: utf-8 -*-
from mocker import MockerTestCase
from pynextcaller.client import OauthClient, BasicAuthClient


class BaseTestCase(MockerTestCase):

    class FakeResponse(object):
        pass

    def __init__(self, *args, **kwargs):
        super(BaseTestCase, self).__init__(*args, **kwargs)
        self.oauth_client = None
        self.basic_client = None
        self.fake_response = None

    def setUp(self):
        oauth_key = 'oauth_key'
        oauth_secret = 'oauth_secret'
        self.oauth_client = OauthClient(oauth_key, oauth_secret)
        self.basic_client = BasicAuthClient(oauth_key, oauth_secret)
        self.fake_response = self.FakeResponse()
        self.fake_response.status_code = 204

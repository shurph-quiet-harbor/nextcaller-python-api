from pynextcaller import items
from pynextcaller.auth import *


class Client(object):
    """The API client."""

    def __init__(self, api_key, api_secret):
        self.auth = BasicAuth(api_key, api_secret)

    def __getattr__(self, name):
        return getattr(items, name)(self)

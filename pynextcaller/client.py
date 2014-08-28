from pynextcaller import items
from pynextcaller.auth import *


class Client(object):
    """The API client."""

    def __init__(self, oauth_key, oauth_secret, auth_class):
        if type(self) is Client:
            raise TypeError("Client class may not be instantiated directly")
        self.auth = auth_class(oauth_key, oauth_secret)

    def __getattr__(self, name):
        return getattr(items, name)(self)


class OauthClient(Client):
    """The Oauth API client."""

    def __init__(self, oauth_key, oauth_secret):
        super(OauthClient, self).__init__(
            oauth_key, oauth_secret, OauthAuth)


class BasicAuthClient(Client):
    """The Basic Auth API client."""

    def __init__(self, oauth_key, oauth_secret):
        super(BasicAuthClient, self).__init__(
            oauth_key, oauth_secret, BasicAuth)

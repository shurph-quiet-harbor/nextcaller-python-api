from __future__ import unicode_literals
from base64 import b64encode


__all__ = (
    'BasicAuth',
)


class BasicAuth(object):
    """Basic auth class"""
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def get_headers(self):
        """Prepare auth_headers"""
        value = b64encode(
            ("%s:%s" % (self.api_key, self.api_secret)).encode('utf-8')
        ).decode('utf-8')
        return {'Authorization': 'Basic %s' % value}

    def __call__(self):
        return self.get_headers()

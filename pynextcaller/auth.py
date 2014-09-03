from base64 import b64encode


__all__ = (
    'BasicAuth',
)


def get_basic_authorization_headers(api_key, api_secret):
    value = b64encode(
        ("%s:%s" % (api_key, api_secret)).encode('utf-8')
    ).decode('utf-8')
    return {'Authorization': 'Basic %s' % value}


class BasicAuth(object):

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def get_headers(self):
        return get_basic_authorization_headers(
            self.api_key, self.api_secret)

    def __call__(self):
        return self.get_headers()

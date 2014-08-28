import hmac
import random
import string
from base64 import b64encode
from hashlib import sha1
import time
try:
    from urlparse import urlparse, parse_qsl, urlunparse
except ImportError:
    from urllib.parse import urlparse, parse_qsl, urlunparse
try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote


__all__ = (
    'BasicAuth',
    'OauthAuth',
)


def _ensure_unicode(s):
    if not isinstance(s, bytes):
        return s.encode('utf-8')
    return s.decode('utf-8')


def _escape(s):
    return quote(_ensure_unicode(s), safe='~').encode('utf-8')


def _get_nonce(length=10):
    symbols = string.ascii_letters + string.digits
    return ''.join([random.choice(symbols) for _ in xrange(length)])


def _get_basic_authorization_headers(oauth_key, oauth_secret):
    return b64encode(
        ("%s:%s" % (oauth_key, oauth_secret)).encode('utf-8')
    ).decode('utf-8')


def get_basic_authorization_headers(oauth_key, oauth_secret):
    return {
        'Authorization': 'Basic %s' % _get_basic_authorization_headers(
            oauth_key, oauth_secret)
    }


def _get_oauth_authorization_headers(oauth_secret, data, url, method='get'):
    parsed_url = urlparse(url)
    url_params = parse_qsl(parsed_url.query)
    realm = _escape(urlunparse(
        (parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', '', '')))
    data = {_escape(key): _escape(value) for (key, value) in data.items()}
    params = data.copy()
    if url_params:
        params.update(
            {_escape(key): _escape(value) for (key, value) in url_params})
    signature_base_string = '&'.join((
        method.upper(),
        realm,
        _escape('&'.join(['%s=%s' % (
            key, params[key]) for key in sorted(params.keys())]))
    ))
    key = '%s&' % _escape(oauth_secret)
    hashed = hmac.new(key, signature_base_string, sha1)
    signature = b64encode(hashed.digest()).decode()
    data['oauth_signature'] = _escape(signature)
    headers = '%s, %s' % (
        'OAuth realm="%s"' % realm,
        ', '.join(['%s="%s"' % (
            key, data[key]) for key in sorted(data.keys())]))
    return {'Authorization': headers}


def get_oauth_authorization_headers(oauth_key, oauth_secret, url, method='get'):
    params = {
        'oauth_consumer_key': oauth_key,
        'oauth_token': '',
        'oauth_signature_method': "HMAC-SHA1",
        'oauth_timestamp': str(int(time.time())),
        'oauth_nonce': _get_nonce(),
        'oauth_version': '1.0'
    }
    headers = _get_oauth_authorization_headers(
        oauth_secret, params, url, method)
    return headers


class ApiAuth(object):

    def __init__(self, oauth_key, oauth_secret):
        self.oauth_key = oauth_key
        self.oauth_secret = oauth_secret


class BasicAuth(ApiAuth):

    def __call__(self, *args, **kwargs):
        return get_basic_authorization_headers(
            self.oauth_key, self.oauth_secret)


class OauthAuth(ApiAuth):

    def __call__(self, *args, **kwargs):
        return get_oauth_authorization_headers(
            self.oauth_key, self.oauth_secret, *args, **kwargs)


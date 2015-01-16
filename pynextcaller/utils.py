from __future__ import unicode_literals
import functools
import json
import re
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode
try:
    unicode = unicode
except NameError:
    # 'unicode' is undefined, must be Python 3
    str = str
    unicode = str
    bytes = bytes
    basestring = (str, bytes)
else:
    # 'unicode' exists, must be Python 2
    str = str
    unicode = unicode
    bytes = str
    basestring = basestring
from .constants import *


__all__ = (
    'default_handle_response',
    'validate_phone',
    'validate_profile_id',
    'prepare_url',
    'prepare_base_url',
    'prepare_json_data',
    'check_kwargs',
)


def _handle_json_response(resp):
    return json.loads(resp)


def prepare_json_data(data):
    try:
        return json.dumps(data)
    except (TypeError, ValueError):
        return data


def default_handle_response(resp):
    return _handle_json_response(resp)


def validate_phone(value, length=DEFAULT_PHONE_LENGTH):
    """Validate phone format"""
    if not value:
        raise ValueError(
            'Invalid phone number: {0}. Phone cannot be blank.'.format(value))
    if isinstance(value, int):
        value = str(value)
    if not isinstance(value, basestring):
        raise ValueError(
            'Invalid phone number: {0}. Phone cannot be type of {1}.'.format(
                value, type(value)))
    if not len(value) == length:
        raise ValueError(
            'Invalid phone number: {0}. Phone should has length {1}.'.format(
                value, length))
    if not value.isdigit():
        raise ValueError(
            'Invalid phone number: {0}. '
            'Phone should consists of only digits.'.format(value))


def validate_profile_id(value, length=DEFAULT_PROFILE_ID_LENGTH):
    """Validate profile id format"""
    if not value:
        raise ValueError(
            'Invalid profile id: {0}. Profile id cannot be blank.'.
            format(value))
    if not isinstance(value, basestring):
        raise ValueError(
            'Invalid profile id: {0}. Profile id cannot be type of {1}.'.
            format(value, type(value)))
    if len(value) != length:
        raise ValueError(
            'Invalid profile id: {0}. Profile id should has length {1}.'.
            format(value, length))


def validate_platform_username(value, max_length=MAX_PLATFORM_USERNAME_LENGTH):
    """Validate platform username"""
    if not value:
        raise ValueError(
            'Invalid platform username: {0}. '
            'Username cannot be blank.'.format(value))
    if not isinstance(value, basestring):
        raise ValueError(
            'Invalid platform username: {0}. '
            'Username cannot be type of {1}.'.format(value, type(value)))
    if len(value) > max_length:
        raise ValueError(
            'Invalid platform username: {0}. '
            'Username should has length less '
            'than {1} symbols.'.format(value, max_length))
    if not re.match('^[a-z0-9_]+$', value):
        raise ValueError(
            'Invalid platform username: {0}. '
            'Letters, numbers and underscores '
            'at lower case are allowed for username.'.format(value))


def prepare_url(base_url, path, url_params=None):
    """Prepare url from path and params"""
    if url_params is None:
        url_params = {}
    url = '{0}{1}'.format(base_url,  path)
    if not url.endswith('/'):
        url += '/'
    url_params_str = urlencode(url_params)
    if url_params_str:
        url += '?' + url_params_str
    return url


def prepare_base_url(sandbox=False, version=DEFAULT_API_VERSION):
    """Prepare url from path and params"""
    base_url = BASE_URL.format(version) if not sandbox \
        else BASE_SANDBOX_URL.format(version)
    return base_url


def check_kwargs(*all_args):

    def dec(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for kw in kwargs:
                if kw not in all_args:
                    raise ValueError(
                        'Keyword argument {0} is not allowed'.format(kw))
            return func(*args, **kwargs)
        return wrapper
    return dec


check_kwargs = check_kwargs('debug', 'handler', 'data', 'platform_username')

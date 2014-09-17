from __future__ import unicode_literals
import json
from xml.dom.minidom import parseString
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
from pynextcaller.constants import *


__all__ = (
    'default_handle_response',
    'validate_format',
    'validate_phone',
    'prepare_url',
    'prepare_json_data',
)


def _handle_json_response(resp):
    return json.loads(resp)


def _handle_xml_response(resp):
    return parseString(resp)


def prepare_json_data(data):
    try:
        return json.dumps(data)
    except (TypeError, ValueError):
        return data


def default_handle_response(resp, response_format='json'):
    if response_format == 'json':
        return _handle_json_response(resp)
    if response_format == 'xml':
        return _handle_xml_response(resp)
    return resp


def validate_phone(value, length=DEFAULT_PHONE_LENGTH):
    """Validate phone format"""
    if not value:
        raise ValueError(
            'Invalid phone number: %s. Phone cannot be blank.' % value)
    if isinstance(value, int):
        value = str(value)
    if not isinstance(value, basestring):
        raise ValueError(
            'Invalid phone number: %s. Phone cannot be type of %s.' % (
                value, type(value)))
    if not len(value) == length:
        raise ValueError(
            'Invalid phone number: %s. Phone should has length %s.' % (
                value, length))
    if not value.isdigit():
        raise ValueError(
            'Invalid phone number: %s. '
            'Phone should consists of only digits.' % value)


def validate_format(response_format):
    """Validate response format"""
    if response_format not in RESPONSE_FORMATS:
        raise ValueError(
            'Unsupported format: %s. Supported formats are: %s' % (
                response_format, RESPONSE_FORMATS))


def prepare_url(path, url_params=None):
    """Prepare url from path and params"""
    if url_params is None:
        url_params = {}
    url = '%s%s' % (BASE_URL,  path)
    if not url.endswith('/'):
        url += '/'
    url_params_str = urlencode(url_params)
    if url_params_str:
        url += '?' + url_params_str
    return url

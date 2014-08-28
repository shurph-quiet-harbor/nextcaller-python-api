import json
from xml.dom.minidom import parseString
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode
from pynextcaller.constants import *


class Item(object):

    def __init__(self, client):
        self.client = client

    @staticmethod
    def _prepare_data(data):
        try:
            return json.dumps(data)
        except (TypeError, ValueError):
            return data

    @staticmethod
    def _handle_json_response(resp):
        return json.loads(resp)

    @staticmethod
    def _handle_xml_response(resp):
        return parseString(resp)

    @staticmethod
    def handle_response(resp, response_format='json'):
        if response_format == 'json':
            return Item._handle_json_response(resp)
        if response_format == 'xml':
            return Item._handle_xml_response(resp)
        return resp

    @staticmethod
    def sanitize_phone(value, length=DEFAULT_PHONE_LENGTH):
        if not value:
            raise ValueError(
                'Invalid phone number: %s. Cannot be blank.' % value)
        if isinstance(value, int):
            value = str(value)
        if not isinstance(value, str):
            raise ValueError(
                'Invalid phone number: %s. Cannot be type of %s.' % (
                    value, type(value)))
        if not len(value) == length:
            raise ValueError(
                'Invalid phone number: %s. Should has length %s.' % (
                    value, length))
        if not value.isdigit():
            raise ValueError(
                'Invalid phone number: %s. Should consists of digits.' % value)

    @staticmethod
    def sanitize_format(response_format):
        if response_format not in RESPONSE_FORMATS:
            raise ValueError(
                'Unsupported format: %s. Supported formats are: %s' % (
                    response_format, RESPONSE_FORMATS))

    @staticmethod
    def prepare_url(path, url_params=None):
        if url_params is None:
            url_params = {}
        url = '%s%s' % (BASE_URL,  path)
        if not url.endswith('/'):
            url += '/'
        url_params_str = urlencode(url_params)
        if url_params_str:
            url += '?' + url_params_str
        return url

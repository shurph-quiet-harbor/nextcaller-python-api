from __future__ import unicode_literals
from pynextcaller.auth import *
from pynextcaller.constants import *
from pynextcaller.utils import *
from pynextcaller.transport import make_http_request


class Client(object):
    """The NextCaller API client"""

    def __init__(self, api_key, api_secret):
        self.auth = BasicAuth(api_key, api_secret)

    def get_by_phone(self, phone, debug=False, handler=None):
        """Get profiles by a phone

        position arguments:
            phone       -- 10 digits phone, str ot int

        Keyword arguments:
        debug           -- boolean (default True)
        handler         -- optional function that will be processing
                           the response.
                           position arguments: (response, response_format)
        """
        method = 'GET'
        validate_phone(phone)
        url_params = {
            'phone': phone,
            'format': JSON_RESPONSE_FORMAT,
        }
        url = prepare_url('records', url_params=url_params)
        response = make_http_request(
            self.auth, url, method=method, debug=debug)
        if handler is None:
            handler = default_handle_response
        return handler(response)

    def get_by_profile_id(self, profile_id, debug=False, handler=None):
        """Get profile by a profile id

        position arguments:
            profile_id  -- Profile identifier

        Keyword arguments:
        debug           -- boolean (default True)
        handler         -- optional function that will be processing
                           the response.
                           position arguments: (response, response_format)
        """
        method = 'GET'
        url_params = {
            'format': JSON_RESPONSE_FORMAT
        }
        url = prepare_url('users/%s/' % profile_id, url_params=url_params)
        response = make_http_request(
            self.auth, url, method=method, debug=debug)
        if handler is None:
            handler = default_handle_response
        return handler(response)

    def update_by_profile_id(self, profile_id, data, debug=False, handler=None):
        """Update profile by a profile id

        position arguments:
            profile_id  -- Profile identifier

        Keyword arguments:
        data            -- dictionary with changed data
        debug           -- boolean (default True)
        handler         -- optional function that will be processing
                           the response.
                           position arguments: (response, response_format)
        """
        method = 'POST'
        url_params = {
            'format': JSON_RESPONSE_FORMAT
        }
        url = prepare_url('users/%s/' % profile_id, url_params=url_params)
        data = prepare_json_data(data)
        response = make_http_request(
            self.auth, url, data=data, method=method,
            content_type=JSON_CONTENT_TYPE, debug=debug)
        if handler is None:
            handler = lambda x: x
        return handler(response)

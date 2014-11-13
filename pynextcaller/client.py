from __future__ import unicode_literals
from pynextcaller.auth import *
from pynextcaller.constants import *
from pynextcaller.utils import *
from pynextcaller.transport import make_http_request


class NextCallerClient(object):
    """The NextCaller API client"""

    def __init__(self, username, password,
                 sandbox=False, version=DEFAULT_API_VERSION):
        """
        position arguments:
            username        -- username, api key
            password        -- password, api secret

        Keyword arguments:
            sandbox         -- [True|False] - default False
            version         -- api version - default 'v2'
        """
        self.auth = BasicAuth(username, password)
        self.sandbox = bool(sandbox)
        self.base_url = prepare_base_url(sandbox, version)

    def get_by_phone(self, phone, debug=False, handler=None):
        """Get profiles by a phone

        position arguments:
            phone           -- 10 digits phone, str ot int

        Keyword arguments:
            debug           -- boolean (default True)
            handler         -- optional function that will be processing
                               the response.
                               position arguments: (response)
        """
        method = 'GET'
        validate_phone(phone)
        url_params = {
            'phone': phone,
            'format': JSON_RESPONSE_FORMAT,
        }
        url = prepare_url(self.base_url, 'records', url_params=url_params)
        response = make_http_request(
            self.auth, url, method=method, debug=debug)
        if handler is None:
            handler = default_handle_response
        return handler(response)

    def get_by_profile_id(self, profile_id, debug=False, handler=None):
        """Get profile by a profile id

        position arguments:
            profile_id      -- Profile identifier, str

        Keyword arguments:
            debug           -- boolean (default True)
            handler         -- optional function that will be processing
                               the response.
                               position arguments: (response)
        """
        method = 'GET'
        validate_profile_id(profile_id)
        url_params = {
            'format': JSON_RESPONSE_FORMAT
        }
        url = prepare_url(self.base_url, 'users/{0}/'.format(profile_id),
                          url_params=url_params)
        response = make_http_request(
            self.auth, url, method=method, debug=debug)
        if handler is None:
            handler = default_handle_response
        return handler(response)

    def update_by_profile_id(self, profile_id, data, debug=False, handler=None):
        """Update profile by a profile id

        position arguments:
            profile_id      -- Profile identifier, str
            data            -- dictionary with changed data

        Keyword arguments:
            debug           -- boolean (default True)
            handler         -- optional function that will be processing
                               the response.
                               position arguments: (response)
        """
        method = 'POST'
        validate_profile_id(profile_id)
        url_params = {
            'format': JSON_RESPONSE_FORMAT
        }
        url = prepare_url(self.base_url, 'users/{0}/'.format(profile_id),
                          url_params=url_params)
        data = prepare_json_data(data)
        response = make_http_request(
            self.auth, url, data=data, method=method,
            content_type=JSON_CONTENT_TYPE, debug=debug)
        if handler is None:
            return response
        return handler(response)

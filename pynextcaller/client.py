from __future__ import unicode_literals
from .auth import *
from .constants import *
from .utils import *
from .transport import make_http_request


class NextCallerClient(object):
    """The NextCaller API client"""

    def __init__(self, username, password,
                 sandbox=False, version=DEFAULT_API_VERSION):
        """
        position arguments:
            username        -- username, api key
            password        -- password, api secret

        Keyword arguments:
            sandbox         -- [True|False] (default False)
            version         -- api version (default 'v2')
        """
        self.auth = BasicAuth(username, password)
        self.sandbox = bool(sandbox)
        self.base_url = prepare_base_url(sandbox, version)

    @check_kwargs
    def get_by_phone(self, phone, **kwargs):
        """Get profiles by a phone

        position arguments:
            phone               -- 10 digits phone, str ot int

        Keyword arguments:
            debug               -- boolean (default True)
            handler             -- optional function that will be processing
                                the response.
                                position arguments: (response)
        """
        validate_phone(phone)
        debug = kwargs.pop('debug', None)
        handler = kwargs.pop('handler', None)
        url_params = dict({
            'phone': phone,
            'format': JSON_RESPONSE_FORMAT,
        }, **kwargs)
        url = prepare_url(self.base_url, 'records/', url_params=url_params)
        response = make_http_request(
            self.auth, url, method='GET', debug=debug)
        if not callable(handler):
            return default_handle_response(response)
        return handler(response)

    @check_kwargs
    def get_by_profile_id(self, profile_id, **kwargs):
        """Get profile by a profile id

        position arguments:
            profile_id          -- Profile identifier, str, length is 30

        Keyword arguments:
            debug               -- boolean (default True)
            handler             -- optional function that will be processing
                                the response.
                                position arguments: (response)
        """
        validate_profile_id(profile_id)
        debug = kwargs.pop('debug', None)
        handler = kwargs.pop('handler', None)
        url_params = dict({
            'format': JSON_RESPONSE_FORMAT
        }, **kwargs)
        url = prepare_url(self.base_url, 'users/{0}/'.format(profile_id),
                          url_params=url_params)
        response = make_http_request(
            self.auth, url, method='GET', debug=debug)
        if not callable(handler):
            return default_handle_response(response)
        return handler(response)

    @check_kwargs
    def update_by_profile_id(self, profile_id, data, **kwargs):
        """Update profile by a profile id

        position arguments:
            profile_id          -- Profile identifier, str, length is 30
            data                -- dictionary with changed data

        Keyword arguments:
            debug               -- boolean (default True)
            handler             -- optional function that will be processing
                                the response.
                                position arguments: (response)
        """
        validate_profile_id(profile_id)
        debug = kwargs.pop('debug', None)
        handler = kwargs.pop('handler', None)
        url_params = dict({
            'format': JSON_RESPONSE_FORMAT
        }, **kwargs)
        url = prepare_url(self.base_url, 'users/{0}/'.format(profile_id),
                          url_params=url_params)
        data = prepare_json_data(data)
        response = make_http_request(
            self.auth, url, data=data, method='POST',
            content_type=JSON_CONTENT_TYPE, debug=debug)
        if not callable(handler):
            return response
        return handler(response)

    @check_kwargs
    def get_fraud_level(self, phone, **kwargs):
        """Get fraud level for phone

        position arguments:
            phone               -- 10 digits phone, str ot int

        Keyword arguments:
            debug               -- boolean (default True)
            handler             -- optional function that will be processing
                                the response.
                                position arguments: (response)
        """
        validate_phone(phone)
        debug = kwargs.pop('debug', None)
        handler = kwargs.pop('handler', None)
        url_params = dict({
            'phone': phone,
            'format': JSON_RESPONSE_FORMAT,
        }, **kwargs)
        url = prepare_url(self.base_url, 'fraud/', url_params=url_params)
        response = make_http_request(
            self.auth, url, method='GET', debug=debug)
        if not callable(handler):
            return default_handle_response(response)
        return handler(response)


class NextCallerPlatformClient(NextCallerClient):
    """The NextCaller platform API client"""

    @check_kwargs
    def get_by_phone(self, phone, **kwargs):
        """Get profiles by a phone

        position arguments:
            phone               -- 10 digits phone, str ot int

        Keyword arguments:
            platform_username   -- platform username, str. Mandatory.
            debug               -- boolean (default True)
            handler             -- optional function that will be processing
                                the response.
                                position arguments: (response)
        """
        if not kwargs.get('platform_username'):
            raise ValueError('Absent platform_username parameter')
        return super(NextCallerPlatformClient, self).\
            get_by_phone(phone, **kwargs)

    @check_kwargs
    def get_by_profile_id(self, profile_id, **kwargs):
        """Get profile by a profile id

        position arguments:
            profile_id          -- Profile identifier, str, length is 30

        Keyword arguments:
            platform_username   -- platform username, str. Mandatory.
            debug               -- boolean (default True)
            handler             -- optional function that will be processing
                                the response.
                                position arguments: (response)
        """
        if not kwargs.get('platform_username'):
            raise ValueError('Absent platform_username parameter')
        return super(NextCallerPlatformClient, self).\
            get_by_profile_id(profile_id, **kwargs)

    @check_kwargs
    def update_by_profile_id(self, profile_id, data, **kwargs):
        """Update profile by a profile id

        position arguments:
            profile_id          -- Profile identifier, str, length is 30
            data                -- dictionary with changed data

        Keyword arguments:
            platform_username   -- platform username, str. Mandatory.
            debug               -- boolean (default True)
            handler             -- optional function that will be processing
                                the response.
                                position arguments: (response)
        """
        if not kwargs.get('platform_username'):
            raise ValueError('Absent platform_username parameter')
        return super(NextCallerPlatformClient, self).\
            update_by_profile_id(profile_id, data, **kwargs)

    def get_platform_statistics(self, page=1, debug=False, handler=None):
        """Get platform statistics

        Keyword arguments:
            debug               -- boolean (default True)
            handler             -- optional function that will be processing
                                the response.
                                position arguments: (response)
        """
        if not isinstance(page, int) or page < 1:
            raise ValueError('Wrong page parameter: {}'.format(page))
        url_params = {
            'format': JSON_RESPONSE_FORMAT,
            'page': page
        }
        url = prepare_url(
            self.base_url, 'platform_users/', url_params=url_params)
        response = make_http_request(
            self.auth, url, method='GET', debug=debug)
        if not callable(handler):
            return default_handle_response(response)
        return handler(response)

    def get_platform_user(self, platform_username, debug=False, handler=None):
        """Get platform user

        position arguments:
            platform_username   -- platform username, str.

        Keyword arguments:
            debug               -- boolean (default True)
            handler             -- optional function that will be processing
                                the response.
                                position arguments: (response)
        """
        url_params = {
            'format': JSON_RESPONSE_FORMAT
        }
        url_path = 'platform_users/{0}/'.format(platform_username)
        url = prepare_url(self.base_url, url_path, url_params=url_params)
        response = make_http_request(
            self.auth, url, method='GET', debug=debug)
        if not callable(handler):
            return default_handle_response(response)
        return handler(response)

    def update_platform_user(self, platform_username, data,
                             debug=False, handler=None):
        """Update platform user data

        position arguments:
            platform_username   -- Platform username, str
            data                -- dictionary with changed data

        Keyword arguments:
            debug               -- boolean (default True)
            handler             -- optional function that will be processing
                                the response.
                                position arguments: (response)
        """
        url_params = {
            'format': JSON_RESPONSE_FORMAT
        }
        url = prepare_url(
            self.base_url, 'platform_users/{0}/'.format(platform_username),
            url_params=url_params)
        data = prepare_json_data(data)
        response = make_http_request(
            self.auth, url, data=data, method='POST',
            content_type=JSON_CONTENT_TYPE, debug=debug)
        if not callable(handler):
            return response
        return handler(response)

    def get_fraud_level(self, phone, **kwargs):
        """Get fraud level for phone

        position arguments:
            phone               -- 10 digits phone, str ot int

        Keyword arguments:
            debug               -- boolean (default True)
            handler             -- optional function that will be processing
                                the response.
                                position arguments: (response)
        """
        return super(NextCallerPlatformClient, self).\
            get_fraud_level(phone, **kwargs)

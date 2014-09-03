from pynextcaller.items.base import Item
from pynextcaller.transport import *
from pynextcaller.constants import *


__all__ = (
    'Profile',
)


class Profile(Item):
    """
    Update profile information
    """

    def __call__(self, profile_id, response_format=JSON_RESPONSE_FORMAT,
                 debug=False, handler=None):
        """
        Allowed parameter is profile_id, data:
        profile_id = "XXXXXXXXXXXX"
        data = {
            "some_field": "some_data"
        }
        res = client.Profile(profile_id, data=data)
        """
        return self.get(profile_id, response_format=response_format,
                        debug=debug, handler=handler)

    def get(self, profile_id, response_format=JSON_RESPONSE_FORMAT,
            debug=False, handler=None):
        method = 'GET'
        url_params = {
            'format': response_format
        }
        url = self.prepare_url('users/%s/' % profile_id, url_params=url_params)
        response = make_http_request(
            self.client.auth, url, method=method, debug=debug)
        if handler is None:
            handler = self.handle_response
        return handler(response, response_format)

    def update(self, profile_id, data, debug=False, handler=None):
        method = 'POST'
        url_params = {
            'format': JSON_RESPONSE_FORMAT
        }
        url = self.prepare_url('users/%s/' % profile_id, url_params=url_params)
        data = self._prepare_data(data)
        response = make_http_request(
            self.client.auth, url, data=data, method=method,
            content_type=JSON_CONTENT_TYPE, debug=debug)
        if handler is None:
            handler = lambda x: x
        return handler(response)

from pynextcaller.items.base import Item
from pynextcaller.transport import *
from pynextcaller.constants import *


__all__ = (
    'Phone',
)


class Phone(Item):
    """
    Get information by phone
    """

    def __call__(self, phone, response_format=JSON_RESPONSE_FORMAT,
                 debug=False, handler=None):
        """
        Allowed parameters are phone, format, debug, handler
        res = client.Phone(1221222122)
        Handler - custom function that takes response and response_format
        arguments
        """
        return self.get(phone, response_format=response_format,
                        debug=debug, handler=handler)

    def get(self, phone, response_format=JSON_RESPONSE_FORMAT,
            debug=False, handler=None):
        method = 'GET'
        self.sanitize_format(response_format)
        self.sanitize_phone(phone)
        url_params = {
            'phone': phone,
            'format': response_format,
        }
        url = self.prepare_url('records', url_params=url_params)
        response = make_http_request(
            self.client.auth, url, method=method, debug=debug)
        if handler is None:
            handler = self.handle_response
        return handler(response, response_format)

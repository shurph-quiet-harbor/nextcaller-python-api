from requests import RequestException

from .utils import prepare_json_data
from .constants import DEFAULT_RETRY_AFTER_HEADER


class HttpException(RequestException):
    """
    An error occurred while handling request.
    """
    MESSAGE_ERROR_TYPE = 'Error'

    def __init__(self, response, *args, **kwargs):
        super(HttpException, self).__init__(response=response, *args, **kwargs)
        self.message = self._prepare_message()
        self.content = self._prepare_content()

    def _prepare_message(self):
        return '{} {}: {}'.format(self.response.status_code, self.MESSAGE_ERROR_TYPE, self.response.reason)

    def _prepare_content(self):
        return prepare_json_data(self.response.text)


class ClientHttpException(HttpException):
    """
    Client side error occurred.
    """
    MESSAGE_ERROR_TYPE = 'Client Error'


class ServerHttpException(HttpException):
    """
    Server side error occurred.
    """
    MESSAGE_ERROR_TYPE = 'Server Error'


class TooManyRequestsException(ClientHttpException):
    """
    '429 Too Many Requests' error occurred.
    """

    def __init__(self, response, *args, **kwargs):
        super(TooManyRequestsException, self).__init__(response, *args, **kwargs)
        self.retry_after = self.response.headers[DEFAULT_RETRY_AFTER_HEADER]

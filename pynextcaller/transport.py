import requests
import json
import logging
from pynextcaller.constants import *
from pynextcaller.exceptions import *
from pynextcaller.auth import get_basic_authorization_headers, \
    get_oauth_authorization_headers


__all__ = (
    'make_http_request',
)


LOG = logging.getLogger(__file__)
LOG.addHandler(logging.StreamHandler())


def to_json(content):
    try:
        return json.loads(content)
    except (TypeError, ValueError):
        return content


def debug_log(value, debug=True):
    if debug:
        LOG.setLevel(logging.DEBUG)
        LOG.debug(value)
    else:
        LOG.setLevel(logging.NOTSET)


def prepare_request_data(
        data=None, headers=None, method='GET',
        timeout=None, ssl_verify=False):
    if headers is None:
        headers = {}
    kwargs = {}
    if timeout is None:
        timeout = DEFAULT_REQUEST_TIMEOUT
    kwargs['timeout'] = timeout
    if method == 'POST':
        kwargs['data'] = data
    if method == 'GET':
        kwargs['params'] = data
    kwargs['headers'] = headers
    kwargs['allow_redirects'] = True
    kwargs['verify'] = ssl_verify
    return kwargs


def api_request(
        url, data=None, headers=None, method='GET',
        timeout=None, ssl_verify=False, debug=False):
    kwargs = prepare_request_data(
        data=data, headers=headers, method=method,
        timeout=timeout, ssl_verify=ssl_verify)
    status_code = 500
    content = u''
    try:
        response = requests.request(method, url, **kwargs)
        debug_log(u'Request url: %s' % response.url, debug)
        if method == 'POST':
            debug_log(u'Request body: %s' % response.request.body, debug)
        status_code = response.status_code
        content = response.content
        if status_code >= 400:
            response.raise_for_status()
        return response.text
    except requests.HTTPError as err:
        raise HttpException(status_code, to_json(content), err)
    except requests.RequestException as err:
        raise ConnectionException(err)


def build_headers(auth, url, method='get', user_agent=None, content_type=None):
    headers = auth(url, method=method)
    headers['Connection'] = 'Keep-Alive'
    if content_type is not None:
        headers['ContentType'] = content_type
    if user_agent is not None:
        headers['User-Agent'] = user_agent
    return headers


def make_http_request(auth, url, data=None, method='GET', user_agent=None,
                      content_type=None, debug=False):
    if data is None:
        data = {}
    if user_agent is None:
        user_agent = DEFAULT_USER_AGENT
    headers = build_headers(
        auth, url, method=method, user_agent=user_agent,
        content_type=content_type)
    requests_kwargs = {
        'method': method,
        'headers': headers,
        'data': data,
        'debug': debug
    }
    response = api_request(url, **requests_kwargs)
    return response

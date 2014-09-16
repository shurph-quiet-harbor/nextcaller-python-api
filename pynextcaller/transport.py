import json
import logging
import requests
from pynextcaller.constants import *
from pynextcaller.exceptions import *


__all__ = (
    'api_request',
    'make_http_request',
)


LOG = logging.getLogger(__file__)
LOG.addHandler(logging.StreamHandler())


def _to_json(content):
    try:
        return json.loads(content)
    except (TypeError, ValueError):
        return content


def _debug_log(value, debug=True):
    if debug:
        LOG.setLevel(logging.DEBUG)
        LOG.debug(value)
    else:
        LOG.setLevel(logging.NOTSET)


def _prepare_request_data(
        data=None, headers=None, method='GET',
        timeout=None, ssl_verify=True):
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


def api_request(url, data=None, headers=None, method='GET',
                timeout=None, ssl_verify=True, debug=False):
    kwargs = _prepare_request_data(
        data=data, headers=headers, method=method,
        timeout=timeout, ssl_verify=ssl_verify)
    status_code = 500
    content = u''
    try:
        response = requests.request(method, url, **kwargs)
        _debug_log(u'Request url: %s' % response.url, debug)
        if method == 'POST':
            _debug_log(u'Request body: %s' % response.request.body, debug)
        status_code = response.status_code
        content = response.content
        if status_code >= 400:
            response.raise_for_status()
        return response.text
    except requests.HTTPError as err:
        raise HttpException(status_code, _to_json(content), err)
    except requests.RequestException as err:
        raise ConnectionException(err)


def _build_headers(auth, user_agent=None, content_type=None):
    headers = auth.get_headers()
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
    headers = _build_headers(
        auth, user_agent=user_agent, content_type=content_type)
    requests_kwargs = {
        'method': method,
        'headers': headers,
        'data': data,
        'debug': debug
    }
    response = api_request(url, **requests_kwargs)
    return response

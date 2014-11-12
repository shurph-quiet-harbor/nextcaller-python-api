import logging
import os
from requests import HTTPError, RequestException
from pynextcaller.client import NextCallerClient


logging.basicConfig()
logger = logging.getLogger('nextcaller')


def get_profile_by_phone(username, password, phone_number, sandbox=False):
    client = NextCallerClient(username, password, sandbox=sandbox)
    try:
        response = client.get_by_phone(phone_number, debug=True)
        response_code = response.status_code
        response_message = response.json()
        return response_code, response_message
    except ValueError as err:
        logger.error('Validation Error: {}'.format(err))
    except HTTPError as err:
        response = err.response
        response_code = response.status_code
        # try to parse error json message
        try:
            response_message = response.json()
        except ValueError:
            response_message = response.text
        logger.error(
            'HTTPError. Status code {}. Response message: {}'.
            format(response_code, response_message))
    except RequestException as err:
        logger.error('RequestException. {}'.format(err))


if __name__ == '__main__':
    test_username = 'XXXXX'
    test_password = 'XXXXX'
    test_phone_number = '1211211212'
    result = get_profile_by_phone(
        test_username, test_password, test_phone_number, True)
    if result is not None:
        code, message = result
        logger.info('Got phone by profile. {}'.format(message))

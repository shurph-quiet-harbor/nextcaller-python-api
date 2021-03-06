import logging
from pynextcaller.client import NextCallerClient
from pynextcaller.exceptions import HttpException


logger = logging.getLogger('nextcaller')
handler = logging.StreamHandler()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

username = 'XXXXX'
password = 'XXXXX'
sandbox = True
phone_number = '1211211212'

client = NextCallerClient(username, password, sandbox=sandbox)

# get fraud level
try:
    response_content = client.get_fraud_level(phone_number)
    logger.info(response_content)
except HttpException as err:
    logger.error(
        'Response message: {}'.format(err.message),
    )

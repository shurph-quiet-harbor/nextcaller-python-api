nextcaller-python-api
=====================

[![Build Status](https://travis-ci.org/Nextcaller/nextcaller-python-api.svg?branch=master)](https://travis-ci.org/Nextcaller/nextcaller-python-api)

A Python wrapper around the Nextcaller API.
The library supports python versions 2.6, 2.7, 3.2, 3.3, 3.4

Installation
------------

**Dependencies**:

* requests

**Installation**:

*cloning from the GitHub repo*:

    $ git clone git://github.com/nextcaller/Nextcaller-python-api.git
    $ cd nextcaller-python-api
    $ python setup.py test
    $ python setup.py build
    $ python setup.py install

*use pip with the GitHub repo*:
    
    $ pip install -U --user git+git://github.com/nextcaller/nextcaller-python-api.git

*use pip with pypi*:

    $ pip install -U --user pynextcaller


Example
-------

    import logging
    from requests import HTTPError, RequestException
    from pynextcaller.client import NextCallerClient
    
    
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
    try:
        response_content = client.get_by_phone(phone_number, debug=True)
        logger.info(response_content)
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
    

NextCallerClient
----------------

    username = "XXXXX"
    password = "XXXXX"
    sandbox = False
    version = 'v2'
    from pynextcaller.client import NextCallerClient
    client = NextCallerClient(username, password, sandbox=False, version=version)

**Parameters**:

    username    - username
    password    - password
    sandbox     - [True|False], default False
    version     - api version, default 'v2'


API Items
-------------

### Get profile by phone ###

    res = client.get_by_phone(number, handler=None, debug=False)
    
**Parameters**:
    
    position arguments:
        phone               -- 10 digits phone, str ot int

    Keyword arguments:
        debug               -- boolean (default True)
        handler             -- optional function that will be processing the response.
                               position arguments: (response)

### Get profile by id ###

    res = client.get_by_profile_id(profile_id, handler=None, debug=False)
    
**Parameters**:
    
    position arguments:
        profile_id          -- Profile identifier, str, length is 30

    Keyword arguments:
        debug               -- boolean (default True)
        handler             -- optional function that will be processing the response.
                               position arguments: (response)


### Update profile by id ###

    res = client.update_by_profile_id(profile_id, data, handler=None, debug=False)
    
**Parameters**:

    position arguments:
        profile_id          -- Profile identifier, str, length is 30
        data                -- dictionary with changed data

    Keyword arguments:
        debug               -- boolean (default True)
        handler             -- optional function that will be processing the response.
                               position arguments: (response)

**Example**:

    profile_id = "XXXXXXXXX" 
    data = {
        "email": "test@test.com"
    }
    handler = lambda response: response
    client.update_by_profile_id(profile_id, data=data, handler=handler)

**Response**:

*Returns **204 No Content** response in the case of the successful request.*


Errors handling
---------------

In case of wrong phone number a ValueError exception will be thrown:

    ValueError('Invalid phone number: 1221. .........)

In case of wrong profile id a ValueError exception will be thrown:

    ValueError('Invalid profile id: assw2. .........)

In case of the library gets a response with the http code more or equal 400,
the [requests.exceptions.HTTPError](http://docs.python-requests.org/en/latest/api/#requests.exceptions.HTTPError)
exception is raised.

In the event of a network problem (e.g. DNS failure, refused connection, etc),
the [requests.exceptions.ConnectionError](http://docs.python-requests.org/en/latest/api/#requests.exceptions.ConnectionError)
exception is raised.

If a request times out,
the [requests.exceptions.Timeout](http://docs.python-requests.org/en/latest/api/#requests.exceptions.Timeout)
exception is raised.

If a request exceeds the configured number of maximum redirections, the
[requests.exceptions.TooManyRedirects](http://docs.python-requests.org/en/latest/api/#requests.exceptions.TooManyRedirects)
exception is raised.

All exceptions inherit from the
[requests.exceptions.RequestException](http://docs.python-requests.org/en/latest/api/#requests.exceptions.RequestException).

The library uses underlying python requests package. You can find all possible exceptions here:
[requests.exceptions](http://docs.python-requests.org/en/latest/api/#exceptions)

Notes
------

It is possible to override the default response handler by passing
a handler function as the keyword argument. For example:

    import json

    def response_handler(response):
        return json.loads(response, encoding='ascii')['records']

    result = client.get_by_phone(number, handler=response_handler)

Default handler for **get_by_phone** and **get_by_profile_id** and **get_platform_statistics** methods:

    import json

    def handler(response):
        return json.loads(response)

Default handler for **update_by_profile_id** method is absent.
The request just returns **204 No Content** response.

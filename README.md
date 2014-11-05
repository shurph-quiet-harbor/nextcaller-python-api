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

    from pynextcaller.client import NextCallerClient
    api_key = "XXXXX"
    api_secret = "XXXXX"
    sandbox = False
    phone_number = "121212..."
    client = NextCallerClient(api_key, api_secret, sandbox=sandbox)
    resp = client.get_by_phone(phone_number)
    print resp


NextCallerClient
----------------

    api_key = "XXXXX"
    api_secret = "XXXXX"
    sandbox = False
    from pynextcaller.client import NextCallerClient
    client = NextCallerClient(api_key, api_secret, sandbox=False)

**Parameters**:

    api_key - api key
    api_secret - api secret
    sandbox - sandbox mode


API Items
-------------

### Get profile by phone ###

    res = client.get_by_phone(number, handler=None, debug=False)
    
**Parameters**:
    
    number - phone number
    debug  - [True|False] - default False
    handler - [None] - function, response handler.
    Arguments of the handler function - (response) 

### Get profile by id ###

    res = client.get_by_profile_id(profile_id, handler=None, debug=False)
    
**Parameters**:
    
    profile_id - id of a profile
    debug  - [True|False] - default False
    handler - [None] - function, response handler.
    Arguments of the handler function - (response) 


### Update profile by id ###

    res = client.update_by_profile_id(profile_id, data, handler=None, debug=False)
    
**Parameters**:

    profile_id - id of a profile
    data - data to update
    debug  - [True|False] - default False
    handler - [None] - function, response handler.
    Arguments of the handler function - (response) 

**Example**:

    profile_id = "XXXXXXXXX" 
    data = {
        "email": "test@test.com"
    }
    handler = lambda response: response
    client.update_by_profile_id(profile_id, data, handler)

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

Default handler for **get_by_phone** and **get_by_profile_id** methods:

    import json

    def handler(response):
        return json.loads(response)

Default handler for **update_by_profile_id** method is absent.
The request just returns **204 No Content** response.

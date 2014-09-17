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

    api_key = "XXXXX"
    api_secret = "XXXXX"
    phone_number = "121212..."
    from pynextcaller.client import Client
    client = Client(api_key, api_secret)
    resp = client.get_by_phone(phone_number)
    print resp


Client
-------------

    api_key = "XXXXX"
    api_secret = "XXXXX"
    from pynextcaller.client import Client
    client = Client(api_key, api_secret)

**Parameters**:

    api_key - api key
    api_secret - api secret


API Items
-------------

### Get profile by phone ###

    res = client.get_by_phone(number, response_format='json', handler=None)
    
**Parameters**:
    
    number - phone number
    response_format - [json|xml] - required response format
    handler - [None] - function, response handler.
    Arguments of the handler function - (response, response_format) 

### Get profile by id ###

    res = client.get_by_profile_id(profile_id, response_format='json', handler=None)
    
**Parameters**:
    
    profile_id - id of a profile
    response_format - [json|xml] - required response format
    handler - [None] - function, response handler.
    Arguments of the handler function - (response, response_format) 


### Update profile by id ###

    res = client.update_by_profile_id(profile_id, data, handler=None)
    
**Parameters**:

    profile_id - id of a profile
    data - data to update
    handler - [None] - function, response handler.
    Arguments of the handler function - (response, response_format) 

**Example**:

    profile_id = "XXXXXXXXX" 
    data = {
        "email": "test@test.com"
    }
    handler = lambda response, response_format: response
    client.update_by_profile_id(profile_id, data, handler)

**Response**:

*Returns 204 response in the case of the succesfull request.*
    

Notes
------

It is possible to override the default response handler by passing
a handler function as the keyword argument. For example:

    func = lambda x, y: (x, x, y)
    result = client.get_by_phone(number, handler=func)

Default handler for PhoneItem.get and ProfileItem.get methods and response_format='json':
    
    def handler(response, response_format):
        return json.loads(response)

Default handler for PhoneItem.get and ProfileItem.get methods and response_format='xml': 
    
    def handler(response, response_format):
        return xml.dom.minidom.parseString(response)

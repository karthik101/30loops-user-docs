========
REST API
========

The REST API lets you interact with the 30loops platform and the resources you
host on it. It lets you also manipulate your account and user, and in the
future query all your metrics and log files. You can connect to this API and
build your own client tools.

Quick Reference
===============

All API access is over HTTPS and can be accesed at ``https://api.30loops.net/``.
The first element of the path indicates the version of the API, currently this
defaults to ``/1.0/``. 

Resource API
------------

========================================================  =========  ==============================================
URL                                                       HTTP Verb  Function
========================================================  =========  ==============================================
/1.0/(account)/(label)/                                   GET        `Listing Resources`_
/1.0/(account)/(label)/                                   POST       `Creating Resources`_
/1.0/(account)/(label)/(resource)/                        GET        `Showing Resources`_
/1.0/(account)/(label)/(resource)/                        PUT        `Updating Resources`_
/1.0/(account)/(label)/(resource)/                        DELETE     `Deleting Resources`_
/1.0/(account)/app/(resource)/environment/                GET        `Listing Application Environments`_
/1.0/(account)/app/(resource)/environment/                POST       `Creating Application Environments`_
/1.0/(account)/app/(resource)/environment/(environment)/  GET        `Showing Application Environments`_
/1.0/(account)/app/(resource)/environment/(environment)/  PUT        `Updating Application Environments`_
/1.0/(account)/app/(resource)/environment/(environment)/  DELETE     `Deleting Application Environments`_
========================================================  =========  ==============================================

Request Format
==============

``POST`` and ``PUT`` requests send a JSON_ message as request body and set the
``Content-Type`` header to ``aplication/json``.

Authentication is currently implemented using `HTTP Basic Auth`_. When requesting
a resource without credentials the server challenges the request with a
`WWW-Authenticate: Basic realm=api@30loops.net` response header.

**Request:**

.. sourcecode:: http

    GET /1.0/30loops/ HTTP/1.1
    Host: api.30loops.net

**Response:**

.. sourcecode:: http

    HTTP/1.0 401 UNAUTHORIZED
    Content-Type: application/json; charset=UTF-8
    WWW-Authenticate: Basic realm=api@30loops.net

Add a ``Authorization`` header to the request to supply the right credentials
(This is an example using the user name *crito* and the password *secret*).

**Request:**

.. sourcecode:: http

    GET /1.0/30loops/ HTTP/1.1
    Authorization: Basic Y3JpdG86c2VjcmV0

Other authentication mechanisms are planned.

.. _`HTTP Basic Auth`: http://en.wikipedia.org/wiki/Basic_access_authentication

Response Format
===============

All response bodies are in JSON_ format. The success of the request is
determined by the status code provided in the response header. Errors are
indicated by a status code of 4XX and success is in the status code range of
2XX. Errors also always return a json message containing 2 fields,
``code`` and ``error``, containg the numerical error code and a message
with more details.

**Response:**

.. sourcecode:: http

    HTTP/1.1 404 NOT FOUND
    Content-Type: application/json; charset=UTF-8

    {
        "code": 404,
        "error": "The requested resource could not be found."
    }

.. _JSON: http://www.json.org/

Resource API
============

There are different types of resources you can create and manage on the 30loops
platform. The type of a resource is determined by its `label`. Currently there
are the following resources available on 30loops:

- :ref:`App resource <app-resource-api>`
- :ref:`App environment <app-environment-api>`
- :ref:`Repository resource <repository-resource-api>`
- :ref:`Database resource <database-resource-api>`
- :ref:`Webserver resource <webserver-resource-api>`

A detailed description of each resource object can be found in the
`Resource Objects`_ section.

.. _`Listing Resources`:

Listing Resources
-----------------

.. http:get:: /1.0/(account)/(label)/

    Retrieve a list of all resources of the type `label` owned by this `account`.

    :param account: The name of a account, a short descriptive word.
    :type account: str
    :param label: The resource type, eg: repository, db, app
    :type label: str
    :status 200: Returns a list of json objects (resources).
    :status 403: Request not permitted.
    :status 404: Account not found.

.. _`Creating Resources`:

Creating Resources
------------------

.. http:post:: /1.0/(account)/(label)/

    Create a new resource of type `label`.

    :param account: The name of a account, a short descriptive word.
    :type account: str
    :param label: The resource type, eg: repository, db, app
    :type label: str
    :status 201: The resource has been succesfully created.

    **Example Request**:

    .. sourcecode:: http
   
        POST /1.0/30loops/repository/ HTTP/1.1
        Authorization: Basic Y3JpdG86c2VjcmV0
        Host: api.30loops.net
        Content-Type: application/json

        {
            "name": "thirty-blog",
            "variant": "git",
            "location": "https://github.com/30loops/thirty-blog/"
        }

    **Example Response:**

    .. sourcecode:: http

        HTTP/1.0 201 CREATED
        Content-Type: application/json; charset=UTF-8
        Location: https://api.30loops.net/1.0/30loops/repository/thirty-blog/
 
When the creation succeeds, a ``201 CREATED`` response is returned, containing
the ``Location`` header with the URI of the new resource.

.. _`Showing Resources`:

Showing Resources
-----------------

.. _`Updating Resources`:

Updating Resources
------------------

.. _`Deleting Resources`:

Deleting Resources
------------------

.. _`Listing Application Environments`:

Listing Application Environments
--------------------------------

.. _`Creating Application Environments`:

Creating Application Environments
---------------------------------

.. _`Showing Application Environments`:

Showing Application Environments
--------------------------------

.. _`Updating Application Environments`:

Updating Application Environments
---------------------------------

.. _`Deleting Application Environments`:

Deleting Application Environmnets
---------------------------------

Resource Objects
================

.. _app-resource-api:

App Resource
------------

.. _app-environment-api:

App Environment
---------------

.. _repository-resource-api:

Repository Resource
-------------------

.. _database-resource-api:

Database Resource
-----------------

.. note::

    Database resources currently can't be created by the user. For each app
    environment you create a database is configured for you automaticaly.

.. _webserver-resource-api:

Webserver Resource
------------------

.. note::

    Webserver resources currently can't be created by the user. For each app
    environment you create a webserver is configured for you automaticaly.

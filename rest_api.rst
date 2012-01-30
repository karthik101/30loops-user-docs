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
/1.0/{account}/{label}/                                   GET        `Listing Resources`_
/1.0/{account}/{label}/                                   POST       `Creating Resources`_
/1.0/{account}/{label}/{resource}/                        GET        `Showing Resources`_
/1.0/{account}/{label}/{resource}/                        PUT        `Updating Resources`_
/1.0/{account}/{label}/{resource}/                        DELETE     `Deleting Resources`_
/1.0/{account}/app/{resource}/environment/                GET        `Listing Application Environments`_
/1.0/{account}/app/{resource}/environment/                POST       `Creating Application Environments`_
/1.0/{account}/app/{resource}/environment/{environment}/  GET        `Showing Application Environments`_
/1.0/{account}/app/{resource}/environment/{environment}/  PUT        `Updating Application Environments`_
/1.0/{account}/app/{resource}/environment/{environment}/  DELETE     `Deleting Application Environments`_
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

    HTTP/1.1 401 UNAUTHORIZED
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

.. http:get:: /1.0/{account}/{label}/

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

.. http:post:: /1.0/{account}/{label}/

    Create a new resource of type `label`.

    :param account: The name of a account, a short descriptive word.
    :type account: str
    :param label: The resource type, eg: repository, db, app
    :type label: str
    :status 201: The resource has been succesfully created.
    :status 400: The request could not be understood by the server.
    :status 403: Request not permitted.

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

        HTTP/1.1 201 CREATED
        Content-Type: application/json; charset=UTF-8
        Location: https://api.30loops.net/1.0/30loops/repository/thirty-blog/
 
When the creation succeeds, a ``201 CREATED`` response is returned, containing
the ``Location`` header with the URI of the new resource.

If the JSON_ input is not valid or isufficient to create a new resource, a
``400 BAD REQUEST`` response is returned by the server.

.. _`Showing Resources`:

Showing Resources
-----------------

.. http:get:: /1.0/{account}/{label}/{resource}/

    Show the details of this `resource`.

    :param account: The name of a account, a short descriptive word.
    :param label: The resource type, eg: repository, db, app
    :param resource: The name of the resource.
    :status 200: Returns the resource as a JSON object.
    :status 403: Request not permitted.
    :status 404: Resource not found.

    **Example Request:**

    .. sourcecode:: http

        GET /1.0/30loops/repository/thirty-blog/ HTTP/1.1
        Authorization: Basic Y3JpdG86c2VjcmV0
        Host: api.30loops.net

    **Example Request:**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json; charset=UTF-8

        {
            "label": "repository", 
            "link": {
                "href": "https://api.30loops.net/1.0/30loops/repository/thirty-blog/", 
                "rel": "self"
            }, 
            "location": "https://github.com/30loops/thirty-blog/", 
            "name": "thirty-blog", 
            "variant": "git"
        }

Each resource can be retrieved by sending a GET request to the resource URI.
The resource URI is returned either when a resources gets created in the
``Location`` header, or in the resource listing of this type.

.. _`Updating Resources`:

Updating Resources
------------------

.. http:put:: /1.0/{account}/{label}/{resource}/

    Update the state of the resource instance.

    :param account: The name of a account, a short descriptive word.
    :param label: The resource type, eg: repository, db, app
    :param resource: The name of the resource.
    :status 200: Returns the updated resource as a JSON object.
    :status 403: Request not permitted.
    :status 404: Resource not found.

    **Example Request:**

    .. sourcecode:: http

        PUT /1.0/30loops/repository/thirty-blog/ HTTP/1.1
        Authorization: Basic Y3JpdG86c2VjcmV0
        Host: api.30loops.net
        Content-Type: application/json

        {
            "location": "https://bitbucket.org/30loops/thirty-blog"
        }

    **Example Response:**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json; charset=UTF-8

        {
            "label": "repository", 
            "link": {
                "href": "/1.0/30loops/repository/thirty-blog/", 
                "rel": "self"
            }, 
            "location": "https://bitbucket.org/30loops/thirty-blog", 
            "name": "thirty-blog", 
            "variant": "git"
        }

To update an existing resource, send a ``PUT`` request with a JSON message in
the request body, containing the changed attributes. Only the attributes that
need to be changed, have to be send in the body. On success, the response
will contain a JSON message in the response body with the updated version of
the resource.

.. note::

    The name of a resource functions as an identifier for this resource. It is
    not possible to change the name of a resource. In that case you have to
    create a new resource and then delete the old one.

.. _`Deleting Resources`:

Deleting Resources
------------------

.. http:delete:: /1.0/{account}/{label}/{resource}/

    Delete the resource..

    :param account: The name of a account, a short descriptive word.
    :param label: The resource type, eg: repository, db, app
    :param resource: The name of the resource.
    :status 200: The resource was succesfully deleted.
    :status 403: Request not permitted.
    :status 404: Resource not found.

    **Example Request:**

    .. sourcecode:: http

        DELETE /1.0/30loops/repository/thirty-blog/ HTTP/1.1
        Authorization: Basic Y3JpdG86c2VjcmV0
        Host: api.30loops.net

    **Example Response:**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json; charset=UTF-8

Sending a ``DELETE`` request to the URI of a resource deletes it.

.. warning::

    This operation **can't** be undone. Once the request returns succesfully, the
    information associated with this resource has been removed on the server
    side.

.. _`Listing Application Environments`:

Listing Application Environments
--------------------------------

.. _`Creating Application Environments`:

Creating Application Environments
---------------------------------

.. _`Showing Application Environments`:

Showing Application Environments
--------------------------------

.. http:get:: /1.0/{account}/app/{resource}/environment/{environment}/

    Show the details of this `environment`.

    :param account: The name of a account, a short descriptive word.
    :param resource: The name of the application.
    :param environment: The name of the environment.
    :status 200: Returns the environment as a JSON object.
    :status 403: Request not permitted.
    :status 404: Environment not found.

    **Example Request:**

    .. sourcecode:: http

        GET /1.0/30loops/app/thirty-blog/environment/production/ HTTP/1.1
        Authorization: Basic Y3JpdG86c2VjcmV0
        Host: api.30loops.net

    **Example Response:**

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json; charset=UTF-8

        {
            "backends": [
                {
                    "count": 3,
                    "region": "eu1"
                }],
            "database": {
                "href": "https://api.30loops.net/1.0/30loops/database/30loops-app-thirty-blog-production/",
                "name": "30loops-app-thirty-blog-production",
                "rel": "related"
            },
            "flavor": "django",
            "install_setup_py": false,
            "link": {
                "href": "https://api.30loops.net/1.0/30loops/app/thirty-blog/environment/production/",
                "rel": "self"
            },
            "name": "production",
            "repo_branch": "master",
            "repo_commit": "HEAD",
            "requirements_file": "requirements"
        }

This retrieves details of an specific environment of an app resource.

.. _`Updating Application Environments`:

Updating Application Environments
---------------------------------

.. _`Deleting Application Environments`:

Deleting Application Environmnets
---------------------------------

Resource Objects
================

Every service that is hosted on 30loops is represented as a resource. A
resource is always created for a certain account. The account is specified in
the URI and does not show up in the JSON representation, neither when creatd
nor when retrieved. Every resource can be retrieved as a JSON object. All
resources have a few common attributes:

**name**
  The name of a resource functions as its identifier. A resource name must be
  unique for an account and a resource label. It is possible for one account to
  have a repository and an app named "thirty-blog", but not to have two apps
  called that way. The name of a resource can't be changed with an update
  request.

**label**
  Each resource has a certain type, that is defined by its label. A label is
  specified in the URI of the resource, eg: /1.0/30loops/app/thirty-blog/,
  where app would be the label. You don't have to specify the label in the JSON
  request when creating a new resource. But the label is part of the
  representation when retrieving the details of a resource.

**variant**
  Each resource type (label) has one or more variants. A variant specifies a
  specific type of this rsource, eg: *postgresql* for databases or *git* for
  repositories.

.. _app-resource-api:

App Resource
------------

The app resource defines web applications that can be hosted on the 30loops
platform. An app specifies a repository and a list of environments that is
associated with this app.

**Example Request:**

.. sourcecode:: http

    GET /1.0/30loops/app/thirty-blog/ HTTP/1.1
    Authorization: Basic Y3JpdG86c2VjcmV0
    Host: api.30loops.net

**Example Response:**

.. sourcecode:: http

    HTTP/1.1 200 OK
    Content-Type: application/json; charset=UTF-8

    {
        "environments": [
            {
                "href": "/1.0/30loops/app/thirty-blog/environment/production/",
                "name": "production",
                "rel": "item"
            }
        ],
        "label": "app",
        "link": {
            "href": "/1.0/30loops/app/thirty-blog/",
            "rel": "self"
        },
        "name": "thrity-blog",
        "repository": {
            "href": "/1.0/30loops/repository/thirty-blog/",
            "name": "thirty-blog",
            "rel": "related"
        },
        "variant": "python"
    }

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

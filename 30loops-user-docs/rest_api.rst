:tocdepth: 2

========
REST API
========

The REST API lets you interact with the 30loops platform and the resources you
host on it. It lets you also manipulate your account and user, and in the
future query all your metrics and log files. You can connect to this API and
build your own client tools.

.. note::

    The API version is currently set to 0.9. While we try to keep the API
    stable, we keep the option open to still change parts of it before freezing
    it in the near future. Especially the JSON format is undergoing some
    changes.

Quick Reference
===============

All API access is over HTTPS and can be accessed at ``https://api.30loops.net/``.
The first element of the path indicates the version of the API, currently this
defaults to ``/0.9/``.

Account API
-----------

===================================================  =========  ==============================================
URL                                                  HTTP Verb  Function
===================================================  =========  ==============================================
/0.9/{account}                                       GET        `Showing Accounts`_
/0.9/{account}/users                                 GET        `Listing Users`_
/0.9/{account}/users                                 POST       `Creating Users`_
/0.9/{account}/users/{username}                      GET        `Showing Users`_
/0.9/{account}/users/{username}                      DELETE     `Deleting Users`_
/0.9/{account}/users/{username}/change_password      PUT        `Change User Password`_
/0.9/{account}/users/{username}/reset_password       POST       `Reset User Password`_
/0.9/{account}/authcheck                             GET        `Testing Credentials`_
===================================================  =========  ==============================================

Resource API
------------

========================================================  =========  ==============================================
URL                                                       HTTP Verb  Function
========================================================  =========  ==============================================
/0.9/{account}/apps                                       GET        `Listing Apps`_
/0.9/{account}/apps                                       POST       `Creating Apps`_
/0.9/{account}/apps/{appname}                             GET        `Showing Apps`_
/0.9/{account}/apps/{appname}                             PUT        `Updating Apps`_
/0.9/{account}/apps/{appname}                             DELETE     `Deleting Apps`_
/0.9/{account}/apps/{appname}/services                    POST       `Creating Services`_
/0.9/{account}/apps/{appname}/services/{service}          GET        `Showing Services`_
/0.9/{account}/apps/{appname}/services/{service}          PUT        `Updating Services`_
/0.9/{account}/apps/{appname}/services/{service}          DELETE     `Deleting Services`_
========================================================  =========  ==============================================

Actions API
-----------

=====================================  =========  ===========================
URL                                    HTTP Verb  Function
=====================================  =========  ===========================
/0.9/{account}/{label}/{resource}      POST       `Queue Action`_
=====================================  =========  ===========================

Logs API
--------

=====================================  =========  ===========================
URL                                    HTTP Verb  Function
=====================================  =========  ===========================
/0.9/{account}/app/{resource}/logs     GET        `Showing Logs`_
=====================================  =========  ===========================

Billing and Usage API
---------------------

=================================================   =========  =============================
URL                                                 HTTP Verb  Function
=================================================   =========  =============================
/0.9/{account}/invoices                             GET        `Listing Invoices`_
/0.9/{account}/invoices/current                     GET        `Showing Current Invoice`_
/0.9/{account}/invoices/{invoice_nr}                GET        `Showing Past Invoices`_
/0.9/{account}/app/{resource}/usage/current         GET        `Showing Current App Usage`_
/0.9/{account}/app/{resource}/usage/{invoice_nr}    GET        `Showing Past App Usage`_
=================================================   =========  =============================

Logbook API
-----------

=====================================  =========  ===========================
URL                                    HTTP Verb  Function
=====================================  =========  ===========================
/0.9/{account}/logbook/{uuid}          GET        `Showing Action Logbook`_
=====================================  =========  ===========================

Request Format
==============

``POST`` and ``PUT`` requests send a JSON_ message as request body and set the
``Content-Type`` header to ``application/json``.

Authentication is currently implemented using `HTTP Basic Auth`_. When requesting
a resource without credentials the server challenges the request with a
``WWW-Authenticate: Basic realm=api@30loops.net`` response header.

**Request:**

.. sourcecode:: http

    GET /0.9/30loops HTTP/1.1
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

    GET /0.9/30loops HTTP/1.1
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

JSON Format
===========

The JSON_ format for all 30loops objects has a similar structure and
implements a certain behavior. The format and behavior described is valid for
all objects identified by an URI. Unless specified in the detailed description
of each object, the rules of this section always apply.

An object is always described as a flat key/value dictionary.

.. code-block:: js

    {
        "name": "thirtyblog",
        "label": "app",
        "variant": "python"
    }

Other objects are referenced again as nested key/value dictionaries.

.. code-block:: js

    {
        "name": "thirtyblog",
        "label": "app",
        "variant": "python",
        "repository": {
            "name": "thirtyblog-repo"
        }
    }

A collection of referenced objects is represented as a list of key/value
dictionaries.

.. code-block:: js

    {
        "name": "thirtyblog",
        "label": "app",
        "variant": "python",
        "repository": {
            "name": "thirtyblog-repo"
        },
        "cnames": [
            {"record": "record1.30loops.net"},
            {"record": "record2.30loops.net"}
        ]
    }

When creating a new object, and you want to reference an already existing
object, its enough to specify the identifier in the JSON request. The
identifier of a resource usually is the `name` of the resource, unless
otherwise specified.

.. code-block:: js

    {
        "name": "thirtyloops-app",
        "repository": {
            "name": "thirtyloops-repo"
        }
    }

.. _`reference-resources`:

If the referenced object with that identifier is not existing, the server
application will try to create it. In that case you have to provide all
necessary fields, as described in the detailed descriptions of the objects
later on in this document. So you can for example create an app resource in the
same moment than the repository resource (This example is shortened, see the
detailed description of `App Resource`_ and `Repository Resource`_ for full
examples).

.. code-block:: js

    {
        "name": "thirtyloops-app",
        "variant": "python",
        "repository": {
            "name": "thirtyloops-repo",
            "variant": "git",
            "location": "https://github.com/30loops/django-on-30loops"
        }
    }

Collections of objects behave the same way. If you specify items in a
collection, the server application will first look for an existing object and
otherwise creates a new one if sufficient input data is supplied.

Referenced objects and collections of referenced objects are rendered in a
short form. Single referenced objects are rendered as a related object, with
the identifier and the URI of the object, and collections are rendered as a
list of items, with the name and URI of the object.

Some collections break this format if it helps the clarity, eg: cnames of an
app.

Fields that are marked optional in the object descriptions can be omitted. They
are not necessary for creating the object and mostly only represent additional
functionality. Fields often also provide a default value. If the field is not
specified in the request message, the server uses the default value instead.
That means you can also omit to specify this field in the request, which saves
bandwidth and typing. Every field except the identifier field (eg, *name* for
resources) can be changed later on.

Changing the object reference to another object **does not** delete the old
object (eg, pointing an app to another repository). The delete has to be done
manually if this is wanted.

Time and Date Formats
=====================

All time and dates that are provided either in a HTTP header or in the body of
a JSON message are given in the following format::

    YYYY-MM-DDTHH:MM:SSZ

eg::

    2012-02-08T11:15:06Z
    2012-04-23T11:56:04+02:00

It follows roughly :rfc:`3339`. All times are given in Amsterdam local time,
and have an UTC offset of +2 hour.

.. _`error-codes`:

Error Messages
==============

All errors are returned with a HTTP status code in the range of 400-599. Each
error response contains the status code and the error message as a JSON message
in the response body, eg:

.. code-block:: javascript

    {
        "code": 403,
        "error": "Bad credentials for crito."
    }

The following error messages are common across the whole API:

- **400**, "Malformed input data.": The request input could not be understood by
  the API. This is mainly due to malformed JSON input.
- **401**, "No authentication provided.": No authentication has been send along
  the request. See _`Request Format` for more information.
- **403**, "Quota reached.": A quota limit has been reached.
- **403**, "Account {account} does not exist.": The account you try to authenticate for
  does not exist.
- **403**, "Account {account} is disabled.": The account is not active.
- **403**, "User {username} does not exist.": The user you try to authenticate with
  does not exist for this account.
- **403**, "Bad credentials for {username}.": The password does not validate.
- **403**, "User {username} is disabled.": The user is not active.
- **404**, "{resource} not found.": The requested resource does not exist.
- **405**, "Method not allowed.": The HTTP method used for the request is not
  valid for this URI.
- **500**, "We encountered an error on the backend. Sorry for that.": A
  unpredicted error occurred. We are really sorry for that.
- **503**, "Service taken down for maintenance.": The API has been temporarily
  disabled.

.. _`account-api`:

Account API
===========

Showing Accounts
----------------

.. http:get:: /0.9/{account}

    Show the details of `account`.

    :param account: The name of a account.
    :status 200: Returns the account as a JSON message.

    **Example Request**:

    .. sourcecode:: http

        GET /0.9/30loops HTTP/1.1
        Authorization: Basic Y3JpdG86c2VjcmV0
        Host: api.30loops.net

    **Example Response:**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json; charset=UTF-8

        {
            "name": "30loops",
            "link": {
                "href": "https://api.30loops.net/0.9/30loops",
                "rel": "self"
            },
            "plan": "STANDARD",
            "plan_upgrade_uri": "https://30loops.chargevault.com/update?key=345f4543334&code=30loops"
        }

Resource Fields
~~~~~~~~~~~~~~~

**name**
  The name of the account

**plan**
  The current pricing plan your account is subscribed to.

**plan_upgrade_uri**
  Visit this URI in your browser to change your subscription.

Listing Users
-------------

.. http:get:: /0.9/{account}/users

    List all users of an account.

    :param account: The name of a account.
    :status 200: Retrieve the list of users.

    **Example Request**:

    .. sourcecode:: http

        GET /0.9/30loops/users HTTP/1.1
        Authorization: Basic Y3JpdG86c2VjcmV0
        Host: api.30loops.net

    **Example Response:**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json; charset=UTF-8

        {
            "items": [
                {
                    "email": "crito@30loops.net",
                    "is_active": true,
                    "link": {
                        "href": "https://api.30loops.net/0.9/30loops/users/crito",
                        "rel": "item"
                    },
                    "username": "crito"
                }
            ],
            "size": 2
        }

Creating Users
--------------

.. http:post:: /0.9/{account}/users

    Create a new user.

    :param account: The name of a account.
    :status 201: The new user has been created.
    :status 400: You have to specify a password.
    :status 405: User already exists.

    **Example Request**:

    .. sourcecode:: http

        POST /0.9/30loops/users HTTP/1.1
        Authorization: Basic Y3JpdG86c2VjcmV0
        Host: api.30loops.net

        {
            "username": "crito",
            "email": "crito@30loops.net",
            "password": "secret"
        }

    **Example Response:**

    .. sourcecode:: http

        HTTP/1.1 201 OK
        Content-Type: application/json; charset=UTF-8
        Location: https://api.30loops.net/0.9/30loops/users/crito

Resource Fields
~~~~~~~~~~~~~~~

**username** (required)
  The username of the user account you want to create.

**email** (required)
  A valid email address for the user account you want to create. This email
  address is also used to recover passwords.

**password** (required)
  The new password for this account.

Showing Users
-------------

.. http:get:: /0.9/{account}/users/{username}

    Show the details of the user `username`.

    :param account: The name of a account.
    :param username: The name of the user.
    :status 200: Returns the user as a json message.

    **Example Request**:

    .. sourcecode:: http

        GET /0.9/30loops/users/crito HTTP/1.1
        Authorization: Basic Y3JpdG86c2VjcmV0
        Host: api.30loops.net

    **Example Response:**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json; charset=UTF-8

        {
            "username": "crito",
            "is_active": true,
            "email": "crito@30loops.net",
            "link": {
                "href": "https://api.30loops.net/0.9/30loops/users/crito",
                "rel": "self"
            }
        }

Resource Fields
~~~~~~~~~~~~~~~

**username**
  The username of the user account you want to create.

**email**
  A valid email address for the user account you want to create. This email
  address is also used to recover passwords.

**is_active**
  A Boolean flag whether this user is active or not.

Deleting Users
--------------

.. http:delete:: /0.9/{account}/users/{username}

    Delete a user.

    :param account: The name of a account.
    :param username: The name of the user.
    :status 204: The user has been deleted.

    **Example Request**:

    .. sourcecode:: http

        DELETE /0.9/30loops/users/crito HTTP/1.1
        Authorization: Basic Y3JpdG86c2VjcmV0
        Host: api.30loops.net

    **Example Response:**

    .. sourcecode:: http

        HTTP/1.1 204 OK
        Content-Type: application/json; charset=UTF-8

Change User Password
--------------------

.. http:put:: /0.9/{account}/users/{username}/change_password

    Update the password for this user.

    :param account: The name of a account.
    :param username: The name of the user.
    :status 204: The password was successfully updated.

    **Example Request**:

    .. sourcecode:: http

        PUT /0.9/30loops/users/crito/change_password HTTP/1.1
        Authorization: Basic Y3JpdG86c2VjcmV0
        Host: api.30loops.net
        Content-Type: application/json

        {
            "password": "new_password"
        }

    **Example Response:**

    .. sourcecode:: http

        HTTP/1.1 204 NO CONTENT
        Content-Type: application/json; charset=UTF-8

Reset User Password
-------------------

.. http:post:: /0.9/{account}/users/{username}/reset_password

    Reset the password for this user. Note that this request needs no
    authentication credentials. A new password will be set and emailed to the
    email address that is associated with this user. See
    `Change User Password`_ how to change your password afterwards.

    :param account: The name of a account.
    :param username: The name of the user.
    :status 204: The password was successfully reset.

    **Example Request**:

    .. sourcecode:: http

        POST /0.9/30loops/users/crito/reset_password HTTP/1.1
        Host: api.30loops.net
        Content-Type: application/json

    **Example Response:**

    .. sourcecode:: http

        HTTP/1.1 204 NO CONTENT
        Content-Type: application/json; charset=UTF-8

Testing Credentials
-------------------

.. http:get:: /0.9/{account}/authcheck

    Check the credentials of a user.

    :param account: The name of a account, a short descriptive word.
    :status 204: The credentials successfully authenticated.

    **Example Request**:

    .. sourcecode:: http

        GET /0.9/30loops/authcheck HTTP/1.1
        Authorization: Basic Y3JpdG86c2VjcmV0
        Host: api.30loops.net
        Content-Type: application/json

    **Example Response:**

    .. sourcecode:: http

        HTTP/1.1 204 NO CONTENT
        Content-Type: application/json; charset=UTF-8

.. _`resource-api`:

Resource API
============

There are two types of resources. Apps and services. A service is always
attached to an app. Currently there are the following services available on
30loops:

- :ref:`Repository resource <repository-resource-api>`
- :ref:`PostgreSQL resource <postgres-resource-api>`
- :ref:`Worker resource <worker-resource-api>`
- :ref:`MongoDB resource <mongodb-resource-api>`

A detailed description of each service can be found in the
`Service Types`_ section. The following labels are currently recognized:

.. _`Listing Aps`:

Listing Apps
------------

.. http:get:: /0.9/{account}/apps

    Retrieve a list of all apps.

    :param account: The name of a account, a short descriptive word.
    :status 200: Returns all apps.

    **Example Request**:

    .. sourcecode:: http

        GET /0.9/30loops/apps HTTP/1.1
        Authorization: Basic Y3JpdG86c2VjcmV0
        Host: api.30loops.net
        Content-Type: application/json

    **Example Response:**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json; charset=UTF-8

        {
            "items": [
                {
                    "cnames": [],
                    "dns_record": "30loops-app-thirtyblog.30loops.net",
                    "envvars": [],
                    "instances": 3,
                    "label": "app",
                    "link": {
                        "href": "https://api.30loops.net/0.9/30loops/apps/thirtyblog",
                        "rel": "item"
                    },
                    "mongodb": {
                        "href": "https://api.30loops.net/0.9/30loops/apps/None/services/mongodb",
                        "rel": "related"
                    },
                    "name": "thirtyblog",
                    "postgres": {
                        "href": "https://api.30loops.net/0.9/30loops/apps/None/services/postgres",
                        "rel": "related"
                    },
                    "published": true,
                    "region": "eu-nl",
                    "repo_commit": "HEAD",
                    "repository": {
                        "href": "https://api.30loops.net/0.9/30loops/apps/None/services/repository",
                        "rel": "related"
                    },
                    "variant": "python",
                    "worker": {
                        "href": "https://api.30loops.net/0.9/30loops/apps/None/services/worker",
                        "rel": "related"
                    }
                }
            ],
            "link": {
                "href": "https://api.30loops.net/0.9/30loops/apps",
                "rel": "self"
            },
            "size": 1
        }

.. _`Creating Apps`:

Creating Apps
-------------

.. http:post:: /0.9/{account}/apps

    Create a new app.

    :param account: The name of a account, a short descriptive word.
    :status 201: The app has been successfully created.

    **Example Request**:

    .. sourcecode:: http

        POST /0.9/30loops/apps HTTP/1.1
        Authorization: Basic Y3JpdG86c2VjcmV0
        Host: api.30loops.net
        Content-Type: application/json

    **Example Response:**

    .. sourcecode:: http

        HTTP/1.1 201 CREATED
        Content-Type: application/json; charset=UTF-8
        Location: https://api.30loops.net/0.9/30loops/apps/thirtyblog

When the creation succeeds, a ``201 CREATED`` response is returned, containing
the ``Location`` header with the URI of the new resource.

.. _`Showing Apps`:

Showing Apps
------------

.. http:get:: /0.9/{account}/apps/{appname}

    Show the details of an app.

    :param account: The name of a account, a short descriptive word.
    :param appname: The name of the app.
    :status 200: Returns the app as a JSON object.

    **Example Request:**

    .. sourcecode:: http

        GET /0.9/30loops/apps/thirtyblog HTTP/1.1
        Authorization: Basic Y3JpdG86c2VjcmV0
        Host: api.30loops.net

    **Example Response:**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json; charset=UTF-8

        {
            "cnames": [],
            "dns_record": "30loops-app-thirtyblog.30loops.net",
            "envvars": [],
            "instances": 3,
            "label": "app",
            "link": {
                "href": "https://api.30loops.net/0.9/30loops/apps/thirtyblog",
                "rel": "self"
            },
            "name": "thirtyblog",
            "postgres": {
                "href": "https://api.30loops.net/0.9/30loops/apps/thirtyblog/services/postgres",
                "rel": "related"
            },
            "published": true,
            "region": "eu-nl",
            "repo_commit": "HEAD",
            "repository": {
                "href": "https://api.30loops.net/0.9/30loops/apps/thirtyblog/services/repository",
                "rel": "related"
            },
            "variant": "python"
        }

.. _`Updating Apps`:

Updating Apps
-------------

.. http:put:: /0.9/{account}/apps/{appname}

    Update the app.

    :param account: The name of a account, a short descriptive word.
    :param appname: The name of the appname.
    :status 200: Returns the updated resource as a JSON object.

    **Example Request:**

    .. sourcecode:: http

        PUT /0.9/30loops/apps/thirtyblog HTTP/1.1
        Authorization: Basic Y3JpdG86c2VjcmV0
        Host: api.30loops.net
        Content-Type: application/json

        {
            "repo_commit": "32ef2cca"
        }

    **Example Response:**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json; charset=UTF-8

        {
            "cnames": [],
            "dns_record": "30loops-app-thirtyblog.30loops.net",
            "envvars": [],
            "instances": 3,
            "label": "app",
            "link": {
                "href": "https://api.30loops.net/0.9/30loops/apps/thirtyblog",
                "rel": "self"
            },
            "name": "thirtyblog",
            "postgres": {
                "href": "https://api.30loops.net/0.9/30loops/apps/thirtyblog/services/postgres",
                "rel": "related"
            },
            "published": true,
            "region": "eu-nl",
            "repo_commit": "32ef2cca",
            "repository": {
                "href": "https://api.30loops.net/0.9/30loops/apps/thirtyblog/services/repository",
                "rel": "related"
            },
            "variant": "python"
        }

To update an existing app, send a ``PUT`` request with a JSON message in
the request body, containing the changed attributes. Only the attributes that
need to be changed, have to be send in the body. On success, the response
will contain a JSON message in the response body with the updated version of
the app.

.. note::

    The name of an app is the identifier. It is not possible to change the name
    of a app. In that case you have to create a new app and delete the old one.

.. _`Deleting Apps`:

Deleting Apps
-------------

.. http:delete:: /0.9/{account}/apps/{appname}

    Delete an app.

    :param account: The name of a account, a short descriptive word.
    :param appname: The name of the app.
    :status 204: The app was successfully deleted.

    **Example Request:**

    .. sourcecode:: http

        DELETE /0.9/30loops/apps/thirtyblog HTTP/1.1
        Authorization: Basic Y3JpdG86c2VjcmV0
        Host: api.30loops.net

    **Example Response:**

    .. sourcecode:: http

        HTTP/1.1 204 NO CONTENT
        Content-Type: application/json; charset=UTF-8

Sending a ``DELETE`` request to the URI of a resource deletes it.

.. warning::

    This operation **can't** be undone. Once the request returns successfully, the
    information associated with this resource has been removed on the server
    side.

.. _`Creating Services`:

Creating Service
----------------

.. http:post:: /0.9/{account}/apps/{appname}/services

    Create a new service for this app.

    :param account: The name of a account, a short descriptive word.
    :param appname: The name of the app.
    :status 201: The service was successfully deleted.

    **Example Request:**

    .. sourcecode:: http

        POST /0.9/30loops/apps/thirtyblog/services HTTP/1.1
        Authorization: Basic Y3JpdG86c2VjcmV0
        Host: api.30loops.net

        {
            "label: "mongodb"
        }

    **Example Response:**

        HTTP/1.1 201 NO CONTENT
        Content-Type: application/json; charset=UTF-8
        Location: https://api.30loops.net/0.9/30loops/apps/thirtyblog/services/mongodb

.. _`Showing Services`:

Showing Services
----------------

.. http:get:: /0.9/{account}/apps/{appname}/services/{service}

    Show a service for this app.

    :param account: The name of a account, a short descriptive word.
    :param appname: The name of the app.
    :param service: The service type.
    :status 200: Returns the service as a JSON object.

    **Example Request:**

    .. sourcecode:: http

        GET /0.9/30loops/apps/thirtyblog HTTP/1.1
        Authorization: Basic Y3JpdG86c2VjcmV0
        Host: api.30loops.net

    **Example Response:**

        HTTP/1.0 200 OK
        Content-Type: application/json; charset=UTF-8

        {
            "host": "10.16.0.100",
            "label": "postgres",
            "link": {
                "href": "https://api.30loops.net/0.9/30loops/apps/thirtyblog/services/postgres",
                "rel": "self"
            },
            "name": "NjlhN2MyN2QyMmN",
            "password": "YWVlNjdmMzlk",
            "port": 9999,
            "published": true,
            "username": "NjlhN2MyN2QyMmN",
            "variant": "postgres_micro"
        }


.. _`Updating Services`:

Updating Service
----------------

.. http:put:: /0.9/{account}/apps/{appname}/services/{service}

    Update a service for this app.

    :param account: The name of a account, a short descriptive word.
    :param appname: The name of the app.
    :param service: The service type.
    :status 200: Returns the updated service as a JSON object.

.. _`Deleting Services`:

Deleting Services
-----------------

.. http:put:: /0.9/{account}/apps/{appname}/services/{service}

    Delete a service for this app.

    :param account: The name of a account, a short descriptive word.
    :param appname: The name of the app.
    :param service: The service type.
    :status 204: The service has been deleted.

Service Types
=============

Resource References
-------------------

Each resource acts as an independent entity. But you can reference different
resources to each other, eg: an App **must** have a repository referenced, but
**may** reference a Database. You can still use the database for your app if
you don't reference it, but then we can't create the
:ref:`instance-environment-label` for you.

You can reference resources with each other by either

#) create the referenced resources at the same time you create the resource
   that holds the reference:

    **Example Request:**

    .. sourcecode:: http

        POST /0.9/30loops/app HTTP/1.1
        Authorization: Basic Y3JpdG86c2VjcmV0
        Host: api.30loops.net
        Content-Type: application/json; charset=UTF-8

        {
            "label": "app",
            "name": "thirty-blog",
            "repository": {
                "name": "thirtyblog",
                "location": "http://github.com/30loops/thirtyblog"
                "variant": "git",
            },
            "variant": "python",
            "region": "ams1"
        }

#) or by setting the reference to the name of an existing resource:

    **Example Request:**

    .. sourcecode:: http

        POST /0.9/30loops/repository HTTP/1.1
        Authorization: Basic Y3JpdG86c2VjcmV0

        {
            "name": "thirtyblog",
            "variant": "git",
            "location": "http://github.com/30loops/thirtyblog"
        }

    .. sourcecode:: http

        POST /0.9/30loops/app HTTP/1.1
        Authorization: Basic Y3JpdG86c2VjcmV0

        {
            "name": "thirtyblog",
            "variant": "python",
            "repository": {
                "name": "thirtyblog",
            },
            "region": "ams1"
        }

.. _app-resource-api:

App Resource
------------

The app resource defines web applications that can be hosted on the 30loops
platform. Every app needs to attach a repository. It can't be created with out
it.

**Example Request:**

.. sourcecode:: http

    GET /0.9/30loops/app/thirtyblog HTTP/1.1
    Authorization: Basic Y3JpdG86c2VjcmV0
    Host: api.30loops.net

**Example Response:**

.. sourcecode:: http

    HTTP/1.1 200 OK
    Content-Type: application/json; charset=UTF-8

    {
        "cnames": [
            {
                "record": "dns1.example.com"
            }
        ],
        "label": "app",
        "dns_record": "30loops-app-thirtyblog.30loops.net",
        "link": {
            "href": "https://api.30loops.net/0.9/30loops/app/thirtyblog",
            "rel": "self"
        },
        "name": "thirty-blog",
        "repository": {
            "href": "https://api.30loops.net/0.9/30loops/repository/thirtyblog",
            "name": "thirtyblog",
            "rel": "related"
        },
        "database": {
            "href": "https://api.30loops.net/0.9/30loops/database/thirtyblog",
            "name": "thirtyblog",
            "rel": "related"
        },
        "variant": "python",
        "instances": 1,
        "repo_commit": "HEAD",
        "region": "ams1"
    }

Resource Fields
~~~~~~~~~~~~~~~

**label** (static, default=app)
  The unique label of this resource.

**variants** (default=python)
  - static
  - python

**name** (identifier)
  The name of this app as identified by the 30loops platform.

**region** (default=ams1)
  The region where to deploy the app to. See the documentation about zones for
  more information.

**repository**
  The referenced repository resource. See the `Repository Resource`_ section
  for more information.

**instances** (default=1)
  Specify the amount of instances you wish to use for this app. It
  defaults to 1 backend. The backends are deployed in the region that you
  specified during app creation.

**repo_commit** (default=HEAD)
  Specify which commit you want to deploy. When deploying an app, this commit
  will be checked out.

**database** (optional)
  The database reference is created automatically when creating an app. Users
  can't create those resources themselves. They are also protected from
  updates. See the section `Database Resource`_ for more information.

**worker** (optional)
  Define a worker resource for your app. See `Worker Resource`_ for more
  information.

**mongodb** (optional)
  Define a MongoDB database for your app. See `MongoDB Resource`_ for more
  information.

**dns_record** (read-only)
  The dns record under the 30loops.net domain that we provide for your app.

**cname_records** (optional)
  A list of cname records that are used to configure the load balancer. Cnames
  are optional. We create as a default a record for your app under the
  30loops.net domain. You should point those cname records to the dns record we
  provide.

.. code-block:: js

    "cname_records": [
        {"record": "cname.example.org"}
    ]

More Examples
~~~~~~~~~~~~~

**App Creation**

This is an example of a minimal app creation, where we create the repository
inline. The response contains a ``Location`` header with the URI of the newly
created resource.

.. sourcecode:: http

    POST /0.9/30loops/app HTTP/1.1
    Authorization: Basic Y3JpdG86c2VjcmV0

    {
        "name": "thirtyblog",
        "variant": "python",
        "repository": {
            "name": "thirtyblog",
            "variant": "git",
            "location": "http://github.com/30loops/thirtyblog"
        },
        "region": "ams1"
    }

.. sourcecode:: http

    HTTP/1.1 201 CREATED
    Content-Type: application/json; charset=UTF-8
    Location: https://api.30loops.net/0.9/30loops/app/thirtyblog

**Connecting a Database**

We have a database resource, called `blogdb` and want to connect it to an app.

.. sourcecode:: http

    PUT /0.9/30loops/app/thirtyblog HTTP/1.1
    Authorization: Basic Y3JpdG86c2VjcmV0

    {
        "name": "thirtyblog",
        "database": {
            "name": "blogdb",
        }
    }

.. sourcecode:: http

    HTTP/1.1 200 OK
    Content-Type: application/json; charset=UTF-8

.. _repository-resource-api:

Repository Resource
-------------------

Every app must have a repository defined. When deploying the repository gets
cloned. It provides the sourcecode for the web application.

**Example Request:**

.. sourcecode:: http

    GET /0.9/30loops/repository/thirtyblog HTTP/1.1
    Authorization: Basic Y3JpdG86c2VjcmV0

**Example Response:**

.. sourcecode:: http

    HTTP/1.1 200 OK
    Content-Type: application/json; charset=UTF-8

    {
        "label": "repository",
        "link": {
            "href": "https://api.30loops.net/0.9/30loops/repository/thirtyblog",
            "rel": "self"
        },
        "location": "https://github.com/30loops/thirtyblog",
        "name": "thirtyblog",
        "variant": "git"
    }

Resource Fields
~~~~~~~~~~~~~~~

**label** (static, default=repository)
  The unique label of this resource.

**variants** (default=git)
  - git

**name** (identifier)
  The name of this repository as identified by the 30loops platform.

**location**
  The full URI where to clone this repository from. This can be any valid
  location identifier understood by your DCVS.

**ssh_key** (optional)
  A ssh key to use when connecting to a repository. This field needs to be a
  base64 encoded string of your password-less private SSH key. Use the
  following command to generate the string (under Linux)::

    base64 -w 0 YOUR_SSH_KEY

.. _postgres-resource-api:

PostgreSQL Resource
-------------------

Currently we offer Postgresql as SQL possibility.

**Example Request:**

.. sourcecode:: http

    GET /0.9/30loops/database/thirtyblog HTTP/1.1
    Authorization: Basic Y3JpdG86c2VjcmV0

**Example Response:**

.. sourcecode:: http

    HTTP/1.1 200 OK
    Content-Type: application/json; charset=UTF-8

    {
        "label": "postgres",
        "link": {
            "href": "https://api.30loops.net/0.9/30loops/database/30loops-db-thirtyblog",
            "rel": "self"
        },
        "name": "30loops-db-thirtyblog",
        "password": "ERd56fZlY2Rh",
        "username": "30loops-db-thirtyblog",
        "variant": "postgres",
        "host": "192.168.0.53",
        "port": 9999
    }

Resource Fields
~~~~~~~~~~~~~~~

**label** (static, default=database)
  The unique label of this resource.

**variants** (default=postgres)
  - postgres

**name** (identifier)
  The name of this database as identified by the 30loops platform.

**password** (read-only)
  The password to access your postgresql database. The password is set by the API
  and the database server is configured accordingly. The password is provided
  within your environment file on your app and worker instances.

**username** (read-only)
  The username to access your postgresql database. The username is set by the API
  and the mongo server is configured accordingly. The username is provided
  within your environment file on your app and worker instances.

**host** (read-only)
  The IP address of the host your database is deployed to. If the database
  hasn't been physically deployed yet, it will say ``not deployed``. The host is
  provided within your environment file on your app and worker instances.

**port** (read-only)
  The port of the postgresql server your database is deployed to. If the database
  hasn't been physically deployed yet, it will say ``not deployed``. The port is
  provided within your environment file on your app and worker instances.

.. _worker-resource-api:

Worker Resource
---------------

Worker resources are used to run different processes. They are in that sense
similar to apps, only they don't run an webserver or application server. But you
can use workers to run cronjobs in the background or for celery task queues.

**Example Request:**

.. sourcecode:: http

    GET /0.9/30loops/worker/thirtyblog HTTP/1.1
    Authorization: Basic Y3JpdG86c2VjcmV0

**Example Response:**

.. sourcecode:: http

    HTTP/1.1 200 OK
    Content-Type: application/json; charset=UTF-8

    {
        "instances": 1,
        "label": "worker",
        "link": {
            "href": "https://api.30loops.net/0.9/30loops/worker/thirtyblog",
            "rel": "self"
        },
        "name": "thirtyblog",
        "variant": "python"
    }

Resource Fields
~~~~~~~~~~~~~~~

**label** (static, default=worker)
  The unique label of this resource.

**variants** (default=python)
  - python

**name** (identifier)
  The name of this worker as identified by the 30loops platform.

**instances** (default=1)
  Specify the amount of instances you wish to use for this worker. It
  defaults to 1 backend. The backends are deployed in the region that you
  specified during app creation.

.. _mongodb-resource-api:

MongoDB Resource
----------------

.. note::

    MongoDB resources currently can't be created directly by the user. They
    always have to defined within the context of an app. See `JSON Format`_
    for more details.

Next to a SQL based database you can also use a MongoDB. Currently instances of
16MB are offered.

**Example Request:**

.. sourcecode:: http

    GET /0.9/30loops/mongodb/thirtyblog HTTP/1.1
    Authorization: Basic Y3JpdG86c2VjcmV0

**Example Response:**

.. sourcecode:: http

    HTTP/1.1 200 OK
    Content-Type: application/json; charset=UTF-8

    {
        "label": "mongodb",
        "link": {
            "href": "https://api.30loops.net/0.9/30loops/mongodb/30loops-mongodb-thirtyblog",
            "rel": "self"
        },
        "name": "30loops-mongodb-thirtyblog",
        "password": "OWQ3YjZlY2Rh",
        "username": "30loops-mongodb-thirtyblog",
        "variant": "16MB",
        "host": "not deployed",
        "port": "not deployed"
    }

Resource Fields
~~~~~~~~~~~~~~~

**label** (static, default=mongodb)
  The unique label of this resource.

**variants** (default=16MB)
  - 16MB

**name** (identifier)
  The name of this mongodb as identified by the 30loops platform.

**password** (read-only)
  The password to access your mongodb database. The password is set by the API
  and the mongo server is configured accordingly. The password is provided
  within your environment file on your app and worker instances.

**username** (read-only)
  The username to access your mongodb database. The username is set by the API
  and the mongo server is configured accordingly. The username is provided
  within your environment file on your app and worker instances.

**host** (read-only)
  The ip address of the host your database is deployed to. If the database
  hasn't been physically deployed yet, it will say ``not deployed``. The host is
  provided within your environment file on your app and worker instances.

**port** (read-only)
  The port of the mongodb server your database is deployed to. If the database
  hasn't been physically deployed yet, it will say ``not deployed``. The port is
  provided within your environment file on your app and worker instances.

Actions API
===========

To interact with the physical state of your resources you can use the actions
API. Each resource can have several actions defined, of things you can do with
it on the platform. While the :ref:`Resource API <resource-api>` focuses on the
configuration part of your resources, the actions API manipulates the physical
state.

Every request to the actions API creates a *logbook* that can be polled for the
progress of the action. The logbook contains the current status of the action,
and the log output generated by the server. If an action has been successfully
queued, the response contains a :mailheader:`Location` header field, containing
the URI of the logbook. See the :ref:`Logbook API <logbook-api>` section for more information on
the logbook.

Action JSON Format
------------------

The API works always the same. You send a ``POST`` request to the resource URI.
In the body of the request you attach a JSON message containing configuration
options that apply to the action. The JSON message format is always the same
and varies only in the options provided.

.. sourcecode:: js

    {
        "action": "deploy",
        "options": {
            // your options here
        }
    }

**action**
  The name of the action to execute. See `Actions`_ for a description of all
  available actions.

**options**
  All configuration variables are defined in this section. See the description
  of each action for all available options.

.. _action-queue-api:

Queue Action
------------

.. http:post:: /0.9/{account}/{label}/{resource}

    Queue an action for this resource.

    :param account: The name of a account, a short descriptive word.
    :param label: The resource type, eg: repository, db, app
    :param resource: The name of the resource.
    :status 202: The action was successfully queued.

    **Example Request:**

    .. sourcecode:: http

        POST /0.9/30loops/app/thirtyloops HTTP/1.1
        Authorization: Basic Y3JpdG86c2VjcmV0
        Host: api.30loops.net

        {
            "action": "deploy",
        }

    **Example Response:**

    .. sourcecode:: http

        HTTP/1.1 202 OK
        Content-Type: application/json; charset=UTF-8
        Location: http://api.30loops.net/0.9/30loops/logbook/0.95af0e-5250-11e1-b660-568837fa3205

Actions
=======

Deploy Action
-------------

**Target Resources:** app

After you configured an application, you can deploy it to the platform.

**Example Request:**

.. sourcecode:: http

    POST /0.9/30loops/app/thirtyblog HTTP/1.1
    Authorization: Basic Y3JpdG86c2VjcmV0
    Host: api.30loops.net

    {
        "action": "deploy",
        "options": {
            "clean": True
        }
    }

**Example Response:**

.. sourcecode:: http

    HTTP/1.1 202 ACCEPTED
    Content-Type: application/json; charset=UTF-8
    Location: https://api.30loops.net/0.9/30loops/logbook/1694a4a0-5bbd-11e1-8fb5-0.99507dbcf2

**action:** deploy

**options:**

*clean* (default=False, Boolean)
  Perform a clean deploy when set to `True`. This means a new bundle will be
  created. If set to False, the old bundle gets reused, and only the source
  code gets updated.

Runcommand Action
-----------------

**Target Resources:** app, worker

You can execute single commands in the context of your application. The command
is executed with your repository as working directory, so if in the root of
your repository you have a file called ``init_db.py`` you can call it with the
command: ``python init_db.py``.

**Example Request:**

.. sourcecode:: http

    POST /0.9/30loops/app/thirtyblog HTTP/1.1
    Authorization: Basic Y3JpdG86c2VjcmV0
    Host: api.30loops.net

    {
        "action": "runcommand",
        "options": {
            "command": "python init_db.py --initial",
            "occurrence": "all"
        }
    }

**Example Response:**

.. sourcecode:: http

    HTTP/1.1 202 ACCEPTED
    Content-Type: application/json; charset=UTF-8
    Location: https://api.30loops.net/0.9/30loops/logbook/1694a4a0-5bbd-11e1-8fb5-0.99507dbcf2

**actions:** runcommand

**options:**

*command* (string)
  The full command to execute.

*occurrence* (default=1, integer or string)
  Specify on how many backends this command should run on. Can be either an
  integer for the number of backends to run it on or ``all``. Defaults to
  ``1``.

Django Management Action
------------------------

**Target Resources:** app, worker

Run a django management command in the context of your django project root. The
working directory of this call is your django project root. You don't have to
specify ``python manage.py`` or a ``--settings`` argument, this happens
automatically for you. So to run ``python manage.py syncdb --settings
production`` you just specify the foll wing command: ``syncdb``.

**Example Request:**

.. sourcecode:: http

    POST /0.9/30loops/app/thirtyblog HTTP/1.1
    Authorization: Basic Y3JpdG86c2VjcmV0
    Host: api.30loops.net

    {
        "action": "djangocommand",
        "options": {
            "command": "syncdb",
            "occurrence": 4
        }
    }

**Example Response:**

.. sourcecode:: http

    HTTP/1.1 202 ACCEPTED
    Content-Type: application/json; charset=UTF-8
    Location: https://api.30loops.net/0.9/30loops/logbook/1694a4a0-5bbd-11e1-8fb5-0.99507dbcf2

**actions:** djangocommand

**options:**

*command* (string)
  The django management command to execute.

*occurrence* (default=1, integer or string)
  Specify on how many backends this command should run on. Can be either an
  integer for the number of backends to run it on or ``all``. Defaults to
  ``1``.

App Scale Instances Action
--------------------------

**Target Resources:** app, worker

You can scale a running app or worker. Scaling means to change the amount of
instances that the app or worker is deployed to. This happens without
interruption to the running instances. To pause an app or worker, you can scale
it to 0 instances

**Example Request:**

.. sourcecode:: http

    POST /0.9/30loops/app/thirtyblog HTTP/1.1
    Authorization: Basic Y3JpdG86c2VjcmV0
    Host: api.30loops.net

    {
        "action": "scale",
        "options": {
            "instances": 3
        }
    }

**Example Response:**

.. sourcecode:: http

    HTTP/1.1 202 ACCEPTED
    Content-Type: application/json; charset=UTF-8
    Location: https://api.30loops.net/0.9/30loops/logbook/1694a4a0-5bbd-11e1-8fb5-0.99507dbcf2

**actions:** scale

**options:**

*instances* (integer or string)
  Specify the number of instances the app or worker should be scaled to. This
  number is the target number of instances you want to end up with.

.. _publish-rest-action:

Publish Action
--------------

**Target Resources:** app

Every app gets created on the free tier per default. To go live with an app,
you have to publish it. That will move it to the paid tier, and lift any
restrictions set on it. This action takes no options.

**Example Request:**

.. sourcecode:: http

    POST /0.9/30loops/app/thirtyblog HTTP/1.1
    Authorization: Basic Y3JpdG86c2VjcmV0
    Host: api.30loops.net

    {
        "action": "publish",
    }

**Example Response:**

.. sourcecode:: http

    HTTP/1.1 202 ACCEPTED
    Content-Type: application/json; charset=UTF-8
    Location: https://api.30loops.net/0.9/30loops/logbook/1694a4a0-5bbd-11e1-8fb5-0.99507dbcf2

**actions:** publish

Restart Action
--------------

**Target Resources:** app, worker

You can restart all processes of your app or worker. This will restart all
daemon processes that run on your instances.

**Example Request:**

.. sourcecode:: http

    POST /0.9/30loops/app/thirtyblog HTTP/1.1
    Authorization: Basic Y3JpdG86c2VjcmV0
    Host: api.30loops.net

    {
        "action": "restart",
    }

**Example Response:**

.. sourcecode:: http

    HTTP/1.1 202 ACCEPTED
    Content-Type: application/json; charset=UTF-8
    Location: https://api.30loops.net/0.9/30loops/logbook/1694a4a0-5bbd-11e1-8fb5-0.99507dbcf2

**actions:** restart

Restore Action
--------------

**Target Resources:** database

You can restore a database with a dump file. The file has to be provided over
a publicly reachable URI. 

The command we use internally to restore the database is:

.. code-block:: bash

    pg_restore --clean --no-acl --no-owner -d <database>

To make sure the database is restored correctly, you should dump your database
with the following command:

.. code-block:: bash

    pg_dump -Fc --no-acl --no-owner <database> > <dumpfile>

**Example Request:**

.. sourcecode:: http

    POST /0.9/30loops/database/30loops-database-blog HTTP/1.1
    Authorization: Basic Y3JpdG86c2VjcmV0
    Host: api.30loops.net

    {
        "action": "restore",
        "options": {
            "location": "http://example.org/file.dump"
        }
    }

**Example Response:**

.. sourcecode:: http

    HTTP/1.1 202 ACCEPTED
    Content-Type: application/json; charset=UTF-8
    Location: https://api.30loops.net/0.9/30loops/logbook/1694a4a0-5bbd-11e1-8fb5-0.99507dbcf2

**actions:** restore

**options:**

*location* (string)
  The HTTP location, where to download the dump file from.

.. _`logs-api`:

Logs API
========

Showing Logs
------------

.. http:get:: /0.9/{account}/app/{resource}/logs

    Retrieve the logs for an app.

    :param account: The name of the account.
    :param resource: The name of the app.
    :query limit: Limit the amount of logs to retrieve. Defaults to 10.
    :query process: Limit the logs to these processes. Supply processes as a
        string separated by a `,`. The following processes can be supplied:

        - nginx
        - gunicorn
        - postgres

        Defaults to 'nginx,gunicorn'.
    :status 200: Returns the log messages.

    **Example Request:**

    .. sourcecode:: http

        GET /0.9/30loops/app/thirtyblog/logs?limit=5,process=gunicorn,nginx HTTP/1.1
        Authorization: Basic Y3JpdG86c2VjcmV0
        Host: api.30loops.net

    **Example Response:**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json; charset=UTF-8

        {
            "messages": [
                {
                    "message": " [error] 2318#0: 41 open() \"/app/static/dfgsdg\" failed (2: No such file or directory), client: 192.168.0.111, server: 30loops-cherrypyonloops-.30loops.net, request: \"GET /static/dfgsdg HTTP/1.1\", host: \"30loops-app-cherrypyonloops.30loops.net\"",
                    "program": "nginx",
                    "severity": "Error",
                    "timestamp": "2012-05-10T12:21:35.857585+00:00"
                },
                {
                    "message": "  File \"/app/env/lib/python2.7/site-packages/gunicorn/arbiter.py\", line 488, in kill_workers",
                    "program": "gunicorn",
                    "severity": "Error",
                    "timestamp": "2012-05-22T15:58:54.3750.9+00:00"
                },
                {
                    "message": "<module 'threading' from '/usr/lib/python2.7/threading.pyc'>",
                    "program": "gunicorn",
                    "severity": "Error",
                    "timestamp": "2012-05-22T15:58:54.376792+00:00"
                },
                {
                    "message": ":",
                    "program": "gunicorn",
                    "severity": "Error",
                    "timestamp": "2012-05-22T15:58:54.376465+00:00"
                },
                {
                    "message": " ignored",
                    "program": "gunicorn",
                    "severity": "Error",
                    "timestamp": "2012-05-22T15:58:54.376949+00:00"
                }
            ]
        }

.. _`billing-usage-api`:

Billing and Usage API
=====================

Listing Invoices
----------------

.. http:get:: /0.9/{account}/invoices

    Retrieve a list of all past invoices. You find here also past usage stats.
    Note the current running invoice is not part of this listing.

    :param account: The name of the account.
    :status 200: Returns the usage stats.

    **Example Request:**

    .. sourcecode:: http

        GET /0.9/30loops/invoices HTTP/1.1
        Authorization: Basic Y3JpdG86c2VjcmV0
        Host: api.30loops.net

    **Example Response:**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json; charset=UTF-8

        {
            "items": [
                {
                    "invoice_number": 1,
                    "link": {
                        "href": "https://api.30loops.net/0.9/30loops/invoices/1",
                        "rel": "item"
                    }
                },
            ],
            "link": {
                "href": "https://api.30loops.net/0.9/30loops/invoices",
                "rel": "self"
            },
            "size": 1
        }

Showing Current Invoice
-----------------------

.. http:get:: /0.9/{account}/invoices/current

    Retrieve the details of the current, running invoice. This invoice has not
    yet been billed, and your current usage is tracked here. You find the
    current resource usage, seperated by free and paid tier.

    :param account: The name of the account.
    :status 200: Returns the usage stats.

    **Example Request:**

    .. sourcecode:: http

        GET /0.9/30loops/invoices/current HTTP/1.1
        Authorization: Basic Y3JpdG86c2VjcmV0
        Host: api.30loops.net

    **Example Response:**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json; charset=UTF-8

        {
            "billing_datetime": "2012-09-15T16:33:56.211000+02:00",
            "created": "2012-08-16T16:33:56.211000+02:00",
            "free": [
                {
                    "item": "Postgresql Micro",
                    "quantity": 3,
                    "unit": "count"
                },
                {
                    "item": "Instance 150MB",
                    "quantity": 6,
                    "unit": "hours"
                }
            ],
            "invoice_number": 4,
            "link": {
                "href": "https://api.30loops.net/0.9/30loops/invoices/4",
                "rel": "self"
            },
            "paid": [
                {
                    "item": "MongoDB Micro",
                    "quantity": 1,
                    "unit": "count"
                },
                {
                    "item": "Instance 150MB",
                    "quantity": 8,
                    "unit": "hours"
                },
                {
                    "item": "Postgresql Micro",
                    "quantity": 2,
                    "unit": "count"
                }
            ]
        }

Showing Past Invoices
---------------------

.. http:get:: /0.9/{account}/invoices/{invoice_nr}

    Retrieve the details of a single invoice. Only usage that is collected on
    the paid tier is shown. Free tier usage is not stored.

    :param account: The name of the account.
    :param invoice_nr: The number of the invoice to retrieve.
    :status 200: Returns the usage stats.

    **Example Request:**

    .. sourcecode:: http

        GET /0.9/30loops/invoices/1 HTTP/1.1
        Authorization: Basic Y3JpdG86c2VjcmV0
        Host: api.30loops.net

    **Example Response:**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json; charset=UTF-8

        {
            "billing_datetime": "2012-08-16T16:33:55.211000+02:00",
            "created": "2012-08-15T17:29:29.117000+02:00",
            "invoice_number": 1,
            "link": {
                "href": "https://api.30loops.net/0.9/30loops/invoices/1",
                "rel": "self"
            },
            "paid": [
                {
                    "item": "Instance 150MB",
                    "quantity": 1503,
                    "unit": "hours"
                },
                {
                    "item": "Postgresql Micro",
                    "quantity": 1,
                    "unit": "count"
                }
            ]
        }

Showing Current App Usage
-------------------------

.. http:get:: /0.9/{account}/app/{resource}/usage/current

    Retrieve the current usage statistics for a specific resource. Usage is
    seperated between free and paid tier.

    :param account: The name of the account.
    :param resource: The name of the app.
    :status 200: Returns the usage stats.

    **Example Request:**

    .. sourcecode:: http

        GET /0.9/30loops/app/thirtyblog/usage/current HTTP/1.1
        Authorization: Basic Y3JpdG86c2VjcmV0
        Host: api.30loops.net

    **Example Response:**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json; charset=UTF-8

        {
            "billing_datetime": "2012-09-15T16:33:56.211000+02:00", 
            "created": "2012-08-16T16:33:56.211000+02:00", 
            "free": {
                "item": "Instance 150MB", 
                "quantity": 3, 
                "unit": "hours"
            }, 
            "invoice_number": 4, 
            "link": {
                "href": "https://api.30loops.net/0.9/30loops/app/thirtyblog/usage/current", 
                "rel": "self"
            }, 
            "paid": {
                "item": "Instance 150MB", 
                "quantity": 2, 
                "unit": "hours"
            }
        }

Showing Past App Usage
----------------------

.. http:get:: /0.9/{account}/app/{resource}/usage/{invoice_nr}

    Retrieve past usage statistics for a specific resource. Usage is
    seperated between free and paid tier. The invoice_nr is synced with the
    invoice number (see above). If you delete a resource, historical usage data
    is deleted too.

    :param account: The name of the account.
    :param resource: The name of the app.
    :param invoice_nr: Query the billing cycle with this invoice number.
    :status 200: Returns the usage stats.

    **Example Request:**

    .. sourcecode:: http

        GET /0.9/30loops/app/thirtyblog/usage/3 HTTP/1.1
        Authorization: Basic Y3JpdG86c2VjcmV0
        Host: api.30loops.net

    **Example Response:**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json; charset=UTF-8

        {
            "billing_datetime": "2012-09-15T16:33:56.211000+02:00", 
            "created": "2012-08-16T16:33:56.211000+02:00", 
            "invoice_number": 3, 
            "link": {
                "href": "https://api.30loops.net/0.9/30loops/app/thirtyblog/usage/3", 
                "rel": "self"
            }, 
            "paid": {
                "item": "Instance 150MB", 
                "quantity": 2, 
                "unit": "hours"
            }
        }

.. _`logbook-api`:

Logbook API
===========

Showing Action Logbook
----------------------

.. http:get:: /0.9/{account}/logbook/{uuid}

    Retrieve the whole logbook with that uuid.

    :param account: The name of a account, a short descriptive word.
    :param uuid: The UUID of the logbook.
    :status 200: Returns the logbook as a JSON object.

    **Example Request:**

    .. sourcecode:: http

        GET /0.9/30loops/logbook/eb920556-5197-11e1-bf5b-568837fa3205 HTTP/1.1
        Authorization: Basic Y3JpdG86c2VjcmV0
        Host: api.30loops.net

    **Example Response:**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json; charset=UTF-8

        {
            "action": "AppDeployAction",
            "status": "running",
            "link": {
                "href": "https://api.30loops.net/0.9/30loops/logbook/eb920556-5197-11e1-bf5b-568837fa3205",
                "rel": "self"
            },
            "messages": [
                {
                    "asctime": "2012-02-08T11:15:04",
                    "loglevel": 1,
                    "message": "Initiating AppDeployAction [eb920556-5197-11e1-bf5b-568837fa3205]",
                },
                {
                    "asctime": "2012-02-08T11:15:05",
                    "loglevel": 1,
                    "message": "Prerun AppDeployAction [eb920556-5197-11e1-bf5b-568837fa3205]",
                },
                {
                    "asctime": "2012-02-08T11:15:06",
                    "loglevel": 0,
                    "message": "Running AppDeployAction [eb920556-5197-11e1-bf5b-568837fa3205]",
                },
                {
                    "asctime": "2012-02-08T11:15:06",
                    "loglevel": 1,
                    "message": "Computing stage: CreateVirtualenv of AppDeployAction [eb920556-5197-11e1-bf5b-568837fa3205]",
                },
            ]
        }

Every action you queue, creates a logbook that tracks the progress of the
operation. Every step and result gets logged into this logbook. You can
retrieve the logbook. The messages in the logbook are ordered ascending by a
time stamp (``asctime``).

The logbook knows 6 different loglevels that are mapped to a numeric value:

- *debug*: 0
- *info*: 1
- *warning*: 2
- *error*: 3
- *critical*: 4
- *exception*: 5

Further you can retrieve the status of your action from the logbook. An action
can be in the following states:

- *queued*: The action is queued and waiting to be processed.
- *running*: The action is currently in progress.
- *finished*: The action has successfully finished.
- *error*: The action stopped due to an error.

.. _`curl-examples-label`:

Examples with ``curl``
======================

You can control every aspect of the platform using any HTTP client. This is an
example on how to use the unix tool ``curl``, which is widely available on
different unix platforms.

To update the email address of your user type the following command:

.. code-block:: bash

    curl -v -X PUT -k -H "Content-Type: application/json" -u crito https://api.30loops.net/0.9/30loops -d '{
    "email":"newemail@example.org"
    }'

**-v** (optional)
  Use verbose mode. Use this to print the actual request/response headers too.
  Use this for more information, but it is optional.

**-X PUT**
  Use the HTTP PUT verb for the request.

**-k**
  Perform an *insecure* request against an SSL enabled URI endpoint. This
  prevents the request to validate the certificate. See
  http://curl.haxx.se/docs/sslcerts.html for more information on this topic.

**-H "Content-Type: application/json"**
  Add the header to the request. Set the correct content type for the request.

**-u crito**
  Use *crito* as username for the HTTP Basic authentication. ``curl`` will ask
  for your password on the prompt. To specify your password in one go, use the
  following format: ``-u <username>:<password>``.

**https://api.30loops.net/0.9/30loops**
  The URI endpoint to send the request to.

**-d ''**
  Craft the needed JSON message and send it as data in the request body. The
  actual data needs to be valid JSON, enclosed by single quotes (``'``) and
  inside the data use double quotes (``"``).

Most requests return a JSON message as a response. If you have python 2.7+
installed, its very easy to pretty print the response message. Pipe the curl
command through ``python -m json.tool``, eg:

.. code-block:: bash

    ~  curl -X PUT -ucrito -H "Content-Type: application/json" -k https://api.30loops.net/0.9/30loops/users/crito -d '{"email": "crito@30loops.net"}' | python -m json.tool
    Enter host password for user 'crito':
    {
        "email": "crito@30loops.net",
        "is_active": true,
        "link": {
            "href": "https://api.30loops.net/0.9/30loops/users/crito",
            "rel": "self"
        },
        "username": "crito"
    }

Add a new user to your account
------------------------------

To create an new user, run the following command and replace the needed fields
as needed:

.. code-block:: bash

    ~ curl -XPOST -k -H "Content-Type: application/json" -u <USERNAME> https://api.30loops.net/0.9/<ACCOUNT>/users -d '{"username": "<NEW_USERNAME>", "email": "<EMAIL_ADDRESS>", "password": "<NEWPASS>"}'

========
REST API
========

The REST API lets you interact with the 30loops platform and the resources you
host on it. It lets you also manipulate your account and user, and in the
future query all your metrics and log files. You can connect to this API and
build your own client tools.

.. note::

    A resource on the 30loops platform specificially means a service that is
    hosted on the platform, like databases, apps or repositories. To not
    confuse URI resources and 30loops resources, we use different terminology.
    If we use the term `resource` we mean a service hosted by 30loops, and if we
    mean an URI resource, we call it an `object`.

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
``WWW-Authenticate: Basic realm=api@30loops.net`` response header.

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

JSON Format
===========

The JSON_ format for all 30loops objects has a similar structure and
implements a certain behaviour. The format and behaviour described is valid for
all objects identified by an URI. Unless specified in the detailed description
of each object, the rules of this section always apply.

An object is always described as a flat key/value dictionary.

.. code-block:: js

    {
        "name": "thirtyblog",
        "label": "app",
        "variant": "python
    }

Other objects are referenced again as nested key/value dictionaries.

.. code-block:: js

    {
        "name": "thirtyblog",
        "label": "app",
        "variant": "python,
        "repository": {
            "name": "thirtyblog-repo",
        }
    }

A collection of referenced objects is represented as a list of key/value
dictionaries.

.. code-block:: js

    {
        "name": "thirtyblog",
        "label": "app",
        "variant": "python,
        "repository": {
            "name": "thirtyblog-repo",
        },
        "environments": [
            {"name": "production"},
            {"name": "production"}
        ]
    }

When creating a new object, and you want to reference an already existing
object, its enough to specify the identifier in the JSON request.

.. code-block:: js

    {
        "name": "thirtyloops-app",
        "repository": {
            "name": "thirtyloops-repo"
        }
    }

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
            "location": "https://github.com/30loops/thirtyloops-repo/"
        }
    }

Collections of objects behave the same way. If you specify items in a
collection, the server application will first look for an existing object and
otherwise creates a new one if sufficient input data is supplied.

Referenced objects and collections of referenced objects are rendered in a
short form. Single referenced objects are rendered as a related object, with
the identifier and the URI of the object, and collections are rendered as a
list of items, with the name and URI of the object.

.. code-block:: js

    {
        "name": "thirtyloops-app",
        "repository": {
            "rel": "related",
            "name": "thirtyloops-repo",
            "href": "https://api.30loops.net/1.0/30loops/repository/thirtyloops-repos/"
        },
        "environments": [
            {
                "rel": "item",
                "name": "production",
                "href": "https://api.30loops.net/1.0/30loops/app/thirtyloops-app/environment/production/"
                },
            {
                "rel": "item",
                "name": "staging",
                "href": "https://api.30loops.net/1.0/30loops/app/thirtyloops-app/environment/staging/"
                }
        ]
    }

Fields that are marked optional in the object descriptions can be omitted. They
are not necessary for creating the object and mostly onyl represent additional
functionality. Fields often also provide a default value. If the field is not
specified in the request message, the server uses the default value instead.
That means you can also omit to specify this field in the request, which saves
badnwidth and typing. Every field except the identifier field (eg, *name* for
resources) can be changed later on.

Changing the object reference to another object **does not** delete the old
object (eg, pointing an app to another repository). The delete has to be done
manually if this is wanted.

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
            "name": "thirtyblog",
            "variant": "git",
            "location": "https://github.com/30loops/thirtyblog/"
        }

    **Example Response:**

    .. sourcecode:: http

        HTTP/1.1 201 CREATED
        Content-Type: application/json; charset=UTF-8
        Location: https://api.30loops.net/1.0/30loops/repository/thirtyblog/
 
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

        GET /1.0/30loops/repository/thirtyblog/ HTTP/1.1
        Authorization: Basic Y3JpdG86c2VjcmV0
        Host: api.30loops.net

    **Example Request:**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json; charset=UTF-8

        {
            "label": "repository", 
            "link": {
                "href": "https://api.30loops.net/1.0/30loops/repository/thirtyblog/", 
                "rel": "self"
            }, 
            "location": "https://github.com/30loops/thirtyblog/", 
            "name": "thirtyblog", 
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

        PUT /1.0/30loops/repository/thirtyblog/ HTTP/1.1
        Authorization: Basic Y3JpdG86c2VjcmV0
        Host: api.30loops.net
        Content-Type: application/json

        {
            "location": "https://bitbucket.org/30loops/thirtyblog"
        }

    **Example Response:**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json; charset=UTF-8

        {
            "label": "repository", 
            "link": {
                "href": "/1.0/30loops/repository/thirtyblog/", 
                "rel": "self"
            }, 
            "location": "https://bitbucket.org/30loops/thirtyblog", 
            "name": "thirtyblog", 
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

        DELETE /1.0/30loops/repository/thirtyblog/ HTTP/1.1
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

        GET /1.0/30loops/app/thirtyblog/environment/production/ HTTP/1.1
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
                "href": "https://api.30loops.net/1.0/30loops/database/30loops-app-thirtyblog-production/",
                "name": "30loops-app-thirtyblog-production",
                "rel": "related"
            },
            "flavor": "django",
            "install_setup_py": false,
            "link": {
                "href": "https://api.30loops.net/1.0/30loops/app/thirtyblog/environment/production/",
                "rel": "self"
            },
            "name": "production",
            "repo_branch": "master",
            "repo_commit": "HEAD",
            "requirements_file": "requirements",
            "djangoflavor": {
                "django_project_root": "project",
                "django_settings_module": "production",
                "auto_syncdb": false,
                "inject_db": true
                }
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

:name:

    The name of a resource functions as its identifier. A resource name must be
    unique for an account and a resource label. It is possible for one account
    to have a repository and an app named "thirtyblog", but not to have two
    apps called that way. The name of a resource can't be changed with an
    update request.

:label:

    Each resource has a certain type, that is defined by its label. A label is
    specified in the URI of the resource, eg: /1.0/30loops/app/thirtyblog/,
    where app would be the label. You don't have to specify the label in the
    JSON request when creating a new resource. But the label is part of the
    representation when retrieving the details of a resource.

:variant: 

    Each resource type (label) has one or more variants. A variant specifies a
    specific type of this rsource, eg: *postgresql* for databases or *git* for
    repositories.

.. _app-resource-api:

App Resource
------------

The app resource defines web applications that can be hosted on the 30loops
platform. Every app needs to attach a repository. It can't be created with out
it. The app itself is not doing too much by itself. To actualy deploy an app to
the platform, you have to define an environment first. You can create an
environment in the moment you create an app.

**Example Request:**

.. sourcecode:: http

    GET /1.0/30loops/app/thirtyblog/ HTTP/1.1
    Authorization: Basic Y3JpdG86c2VjcmV0
    Host: api.30loops.net

**Example Response:**

.. sourcecode:: http

    HTTP/1.1 200 OK
    Content-Type: application/json; charset=UTF-8

    {
        "environments": [
            {
                "href": "https://api.30loops.net/1.0/30loops/app/thirtyblog/environment/production/",
                "name": "production",
                "rel": "item"
            }
        ],
        "label": "app",
        "link": {
            "href": "https://api.30loops.net/1.0/30loops/app/thirtyblog/",
            "rel": "self"
        },
        "name": "thrity-blog",
        "repository": {
            "href": "https://api.30loops.net/1.0/30loops/repository/thirtyblog/",
            "name": "thirtyblog",
            "rel": "related"
        },
        "variant": "python"
    }

Resource Fields
~~~~~~~~~~~~~~~

**label** (static, default=app)
  The unique label of this resource.
**variants** (default=python) 
  - python
**name** (identifier)
  The name of this app as identified by the 30loops platform.
**repository**
  The referenced repository resource. See the `Repository Resource`_ section
  for more information.
**environments** (optional)
  A collection of environments this app has. See the `App Environment`_ section
  for more information.

More Examples
~~~~~~~~~~~~~

**App Creation**

This is an example of a miniam lapp creation, where we create the repository
and one environment inline. The response contains a ``Location`` header with
the URI of the newly created resource.

.. sourcecode:: http

    POST /1.0/30loops/app/ HTTP/1.1
    Authorization: Basic Y3JpdG86c2VjcmV0

    {
        "name": "thirtyblog",
        "variant": "python",
        "repository": {
            "name": "thirtyblog",
            "variant": "git",
            "location": "http://github.com/30loops/thirtyblog"
        },
        "environments": [{
            "name": "production",
            "flavor": "django",
            "backends": [
                {"region": "eu1", "count": 2}
            ]}    
            ]
    }

.. sourcecode:: http

    HTTP/1.1 201 CREATED
    Content-Type: application/json; charset=UTF-8
    Location: https://api.30loops.net/1.0/30loops/app/thirtyblog/

.. _app-environment-api:

App Environment
---------------

**Example Request:**

.. sourcecode:: http

    GET /1.0/30loops/app/thirtyblog/environment/production/ HTTP/1.1
    Authorization: Basic Y3JpdG86c2VjcmV0

**Example Response:**

.. sourcecode:: http

    HTTP/1.1 200 OK
    Content-Type: application/json; charset=UTF-8

    {
        "backends": [
            {
                "count": 2,
                "region": "eu1"
            },
        ],
        "database": {
            "href": "https://api.30loops.net/1.0/30loops/database/30loops-app-thirtyblog-production/",
            "name": "30loops-app-thirtyblog-production",
            "rel": "related"
        },
        "flavor": "django",
        "install_setup_py": false,
        "link": {
            "href": "https://api.30loops.net/1.0/30loops/app/thirtyblog/environment/production/",
            "rel": "self"
        }, 
        "name": "production", 
        "repo_branch": "master", 
        "repo_commit": "HEAD", 
        "requirements_file": "requirements",
        "djangoflavor": {
            "django_project_root": "project",
            "django_settings_module": "production",
            "auto_syncdb": false,
            "inject_db": true
            }
    }

Resource Fields
~~~~~~~~~~~~~~~

.. note::

    The app environment resource has no variant field. Instead you can choose a
    flavor.

**flavor** (default=wsgi)
  A flavor of a python web application. Current choices are:

  - wsgi
  - django

  Each flavor can define some more fields, that are only valid for that
  specific flavor. See the section about `App Flavors`_ for more information.
    
**install_setup_py** (default=False)
  Specifies if the deploy mechanism should look for a setup.py file in the
  source code root directory, and run a ``python setup.py install``.
**requirements_file** (default=requirements)
  Look for a file containing required package dependencies. This file is looked
  for in the root directory of the source repository. See the `pip
  documentation`_ for more information.
**backends**
  In order to deploy an app environment you have to tell the 30loops platform
  where you want to do that and how many backends you plan on using. The format
  of this collection breaks the standard format for 30loops collections
  described in `JSON Format`_. Its a list of simple dictionaries containing two
  fields:

  - region
  - count

  Region is a unique identifier for an available zone on 30loops. Count
  determines how many backends you want to deploy in that specific region. You
  can specify more than one backend definition::

    ...
    "backends": [
        {"region": "eu1", "count": 2},
        {"region": "eu2", "count": 1},
    ]
    ...

**database**
  The database reference is created automaticaly when creating an app
  environment for the first time. Users can't create those resources
  themselves. They are also protected from updates. See the section
  `Database Resource`_ for more information.

App Flavors
~~~~~~~~~~~

Python application can come in two flavors. Regular WSGI and django
applications. For each flavor you have to define a few more fields. Specify the
flavor options as a referenced resource inside the environment resource.


WSGI Flavor
+++++++++++

WSGI apps are configured by specifying the application entry point::

    ...
    "wsgiflavor": {
        "wsgi_entry_point": "wsgi:app",
        "wsgi_project_root": "project"
    }

**wsgi_entry_point**
  The format of the string should be in the way of module:callable. The module
  must be on the python path, and the callable that gets called for the
  incoming request.

**wsgi_project_root** (default=project)
  Specify the root directory of your wsgi app. This path gets added to the
  python path and is relative to your repository root.

Django Flavor
+++++++++++++

Django apps have a few more specific fields::

    ...
    "djangoflavor": {
        "django_project_root": "project",
        "django_settings_module": "production",
        "auto_syncdb": false,
        "inject_db": true
    }

**django_project_root** (default=project)
  Specify the root directory of your django app. Thos path gets added to the
  python path and is relative to your repository root.

**django_settings_module** (default=settings)
  Specify the module path to your settings file. The settings module must be
  found on the python path. 

**auto_syncdb** (default=False)
  Run automaticaly at the end of a deploy a syncdb command. The default is not
  to, but you can change the behaviour by setting this value to ``True``.

**inject_db** (default=True)
  When deploying an app, the database settings will be automatically appendend
  to the end of your settings file. You can turn this behaviour off by setting
  this field to ``False``.

.. _`pip documentation`: http://www.pip-installer.org/en/latest/requirements.html

.. _repository-resource-api:

Repository Resource
-------------------

Every app must have a repository defined. When deploying the repository gets
cloned. It provides the sourcecode for the webapplication.

**Example Request:**

.. sourcecode:: http

    GET /1.0/30loops/repository/thirtyblog/ HTTP/1.1
    Authorization: Basic Y3JpdG86c2VjcmV0

**Example Response:**

.. sourcecode:: http

    HTTP/1.1 200 OK
    Content-Type: application/json; charset=UTF-8

    {
        "label": "repository",
        "link": {
            "href": "https://api.30loops.net/1.0/30loops/repository/thirtyblog/",
            "rel": "self"
        },
        "location": "https://github.com/30loops/thirtyblog/",
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
**username** (optional)
  Specify the username to use when connecting to the repository, in case it is
  not publicly available.
**password** (optional)
  Specify the password to provide when cloning a repository and it is password
  protected.
**ssh_key** (optional)
  A ssh key to use when connecting to a repository.

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

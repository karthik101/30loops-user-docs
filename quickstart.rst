================
Quickstart guide
================

This guide will take you through the following steps:

#) Installing the 30loops client
#) Creating an application
#) Deploying an application

The 30loops platform abstracts all services you can manage as resources.
Your app is a resource, so is your database or the repository you connect to a
resource. A resource is represented as a json message and has different fields.
You can consult the :doc:`REST API guide <rest_api>` for a detailed description
of each resource.

Each resource has at least the following fields:

- **name**

  The name is a unique identifier. Each resource must have a unique name
  together with the label for this account, eg: You can have an app and a
  repository that both have the name ``blog``. But not two apps, with the same
  name.

- **label**

  Each resource is of a certain type, and each type has a label. For now we
  support the following resource types:

  - app
  - repository
  - database

- **variant**

  Each resource type can be of a variant. For now this is simple since we offer
  for each resource one variant. But this will change in the near future. 

Working on the platform consists mainly of two tasks:

#) Creating, editing and deleting resources

   Here you manipulate the configuration of your resources. You do this by
   sending JSON messages to the API. You can craft those messages by hand or
   use the :doc:`thirty cli tool <thirty-cli>`.

#) Queuing actions for a resource

   This manipulates the physical state of your resources. You can deploy or run
   commands in the context of your resource on the platform. Each resource
   accepts different actions. The ``thirty`` cli tool supports all available
   actions. Otherwise check the :doc:`REST API guide <rest_api>` for a
   detailed description of each action.

You need to have a valid account to use the client.

.. note::

    The quickstart guide is assuming you use the ``thirty`` client command for
    all operations. But you can also craft the necessary JSON messages yourself
    and send them to the HTTP API. Both approaches are equivalent.

Installing the 30loops client
=============================

Communicating with the 30loops platform can be done using the documented REST
api, or using the 30loops client, called thirty. The REST api is documented
here, in this quickstart we will focus on using the client.  You can install
the client using pip::

    pip install thirty-cli

If pip is not available on your system, you need to install it. On any Debian
based system, you can run::

    apt-get install python-pip

The client is still quite rough, right now it just opens an editor with a
preformatted JSON message. You can change the fields, and when you save the
message, it will be validated and sent to the API. To define the editor of your
choice, you need to export the EDITOR in your environment. For linux, this can
be done by running the following command::

   export EDITOR=vim

You can specify the editor of your choice. In Windows it can be done by
running::

   set EDITOR=c:/winnt/notepad.exe

Creating an application
=======================

.. note::

    At the moment the client will enable you to edit your resources using a
    text editor. You have to edit valid json messages. A common error is to
    leave a ``,`` after the last field, which doesn't validates as correct
    json. Try to avoid the following::

        {
            "name": "appname",
            "field": "value",  // <-- Note the trailing comma, it will raise an
                               //     error. Avoid a trailing coma after the last
                               //     field.
        }

An application on 30loops consists of the following components:

- A repository resource
- An app resource
- An environment

Applications on 30loops are deployed using a pull mechanism. This means,
30loops will connect to your code repository, fetch the code, and deploy it on
the platform.

You can create these resources seperately are all together in one request. We
first create them seperated, and give you an example of creating an app in one
go leter on.

Creating a repository resource
------------------------------

To create a repository resource run the following command::

    thirty create repository myrepo

The only field that you have to provide for a repository is its ``name`` and
its ``location``. Fill in the location when the editor opens::

    {
        "name": "myrepo",
        "location": "git://github.com/bastichelaar/Django-CMS-30loops.git",
        "variant": "git"
    }

Save and quit the editor, and the repository resource gets created. To verify,
run::

    thirty show repository myrepo
    
It will output something like:

.. code-block:: js

    {
        "link": {
            "href": "http://api.30loops.net/1.0/30loops/repository/myrepo/", 
            "rel": "self"
        }, 
        "location": "git://github.com/bastichelaar/Django-CMS-30loops.git", 
        "variant": "git", 
        "name": "myrepo", 
        "label": "repository"
    }

Creating an app resource
------------------------

Create an app with the following command::

    thirty create app myapp

This will open up the previously specified editor, with the following contents:

.. code-block:: js

    {
        "name": "myapp",
        "variant": "python",
        "repository": {
                "location": "",
                "name": "",
                "variant": "git"
                },
        "environments": []
    }

As you can see, there is a template for a repository already included. You can
either create here a new repository or use the repository we created before.
You could already create the first environment here. But for the purpose of
this example we will do this in a seperate step. We provide later examples for
a complete app, that is created in one step. We fill in the fields in the
following way, save and quit the editor.

.. code-block:: js

    {
        "name": "myapp",
        "variant": "python",
        "repository": {
                "name": "myrepo"
                },
        "environments": []
    }

You can see the configuration of your app so far using the following command::

    thirty show app myapp

It will output something like:

.. code-block:: js

    {
        "name": "myapp", 
        "repository": {
            "href": "http://api.30loops.net/1.0/30loops/repository/myrepo/", 
            "name": "myrepo", 
            "rel": "related"
        }, 
        "variant": "python", 
        "environments": [], 
        "label": "app", 
        "link": {
            "href": "http://api.30loops.net/1.0/30loops/app/myapp/", 
            "rel": "self"
        }
    }

The app resource is now created. We will continue with creating the application
environment.

Creating an environment
-----------------------

You can create one or more environments per app. So it is normal to have a
development, a staging and a production environment. Use the following command
to create an environment::

    thirty create app thirtyblog production

The editor will open up and you'll see something like that::

    {
        "backends": [],
        "cname_records": [],
        "name": "production",
        "repo_branch": "master",
        "repo_commit": "HEAD",
        "requirements_file": "requirements",
        "install_setup_py": false,
        "flavor": "wsgi",
        "djangoflavor": {
            "auto_syncdb": false,
            "django_project_root": "project",
            "django_settings_module": "settings",
            "inject_db": true
        },
        "wsgiflavor": {
            "wsgi_entrypoint": "",
            "wsgi_project_root": "project"
        }
    }

All fields are defined in detail in the :doc:`REST API guide <rest_api>`. We
concentrate here on the important ones, which have to be defined at this point.

The ``backends`` fields contains the number of backends per zone. At this
moment we have the following zone:

#) **eu1**, the default zone in Amsterdam

The format of defining a zone is the following::

    ...
    "backends": [{"region": "eu1", "count": 1}]
    ...

We support two ways of installing application dependencies. You can specify a
requirements file, that is used by ``pip`` to install requirements. See the
`pip website`_ for more information on the format of the requriements file. You
have to specify the requirements with the relative path from the root of your
repository.

You can also provide a setup.py file and specify all dependencies there. The
deploy action will run a ``python setup.py install`` that installs all your
requirements. To enable this behaviour set::

    ...
    "install_setup_py": True
    ...

We support right now two different flavors of python web apps: Django and WSGI.
The details to create an app environment differ a little bit between those two.
Pick from your choice of flavor. Note that frameworks like flask are run as
WSGI apps, and no special support is available at this moment. You have to
choose one of the two flavors and configure its flavor section accordingly.
Set the ``flavor`` field to the right type.

- `Creating a WSGI flavor`_
- `Creating a Django flavor`_

.. _`pip website`: http://www.pip-installer.org/en/latest/requirements.html

Creating a WSGI flavor
~~~~~~~~~~~~~~~~~~~~~~

To create a wsgi based web application edit the environment resource the
following::

    ...
    "flavor": "wsgi",
    "wsgiflavor": {
        "wsgi_entrypoint": "",
        "wsgi_project_root": "project"
    }

The ``wsgi_entrypoint`` field tells us which callable is your entry point for
the webserver. The format is ``module.path:callable``. The
``wsgi_project_root`` field tells us which path relative to the repository root
the application is stored in. 

Creating a Django flavor
~~~~~~~~~~~~~~~~~~~~~~~~

::

    ...
    "flavor": "django",
    "djangoflavor": {
        "auto_syncdb": false,
        "django_project_root": "project",
        "django_settings_module": "settings",
        "inject_db": true
    }

The ``django_project_root`` is the directory where your actual Django
application (the manage.py) lives. The ``django_settings_module`` is the
settings module of your application (used for example in ``python manage.py
syncdb --settings settings``). You can choose to auto inject at the bottom of
your settings file the ``DATABASE`` configuration. If you set ``auto_syncdb``
to true, the deploy script runs automatically a ``python manage.py syncdb``
during your deploy. Otherwise you can run the command manually and keep control
over it.

If you save this file after filling in the correct variables, it will be
validated and sent to the api. To verify if your environment is created
correctly, run::

    thirty show app thirtyblog production

As you can see, the database resource is automatically created. Your
application is now ready for deployment.

Deploying an application
========================

Deploying an application is quite simple and fast, just run the following
command::

    thirty deploy myapp production

This will start the deployment on the number of backends you specified. The
output of the logbook will be fetched and renewed every 10 seconds. You can
also access the logbook manually by running::

    thirty logbook UUID

Where UUID is the ID of the deployment task.

After a successfull deploy, your application will be available on the specified
DNS name and on 30loops.net, for example
``http://30loops-app-myapp-production.30loops.net``.

Additional support
==================

If you have any questions, please log in on ``http://help.30loops.net`` and
submit a ticket. You can also chat with us on #30loops at irc.freenode.net or
mail us at support@30loops.net.

================
Quickstart guide
================

This guide will provide some basic information about the platform and walk you
through the following steps:

#) Basics of the platform
#) Installing the 30loops client
#) Creating an application
#) Deploying an application

We will configure and deploy an example app you can find in our `repository on
github`_. Its a very simple cherrypy application. It already contains a
``thirty.ini`` file, that configures the runtime environment. If you want to
deploy your own apps, you have to provide your own ``thirty.ini`` file. But its
very simple, you can find more information at :ref:`runtime-configuration-label`.

.. _`repository on github`: https://github.com/30loops/cherrypy-on-30loops

30loops basics
==============

An application on 30loops consists of the following components:

- A repository resource
- An app resource

In this quickstart, we will create the application and a repository. You can
create multiple environments per application, for example a staging,
development and production environment. You can also create separate repository
resources that you can connect to an application. We will go more indepth in
the next chapters.

Resources are first configured. Once you have a resource configured you can
issues actions on your resources like ``deploy``. Applications on 30loops are
deployed using a pull mechanism. This means, 30loops will connect to your code
repository, fetch the code, and deploy it on the platform.

You can control every aspect of your application using a JSON API. We provide
for now a command line tool, but feel free to access the API in any means
suitable for you. To use the the platofrm, you need to have a valid, active account.

Installing the 30loops client
=============================

Communicating with the 30loops platform can be done using the documented REST
api, or using the 30loops client, called thirty. The REST api is documented
::doc:`here <rest_api>`, in this quickstart we will focus on using the client.
You can install the client using pip:

.. code-block:: bash

    $ pip install thirty-cli

If pip is not available on your system, you need to install it. On any Debian
based system, you can run:

.. code-block:: bash

    $ apt-get install python-pip

You can also build it from source. Grab the latest copy from
https://github.com/30loops/thirty-cli and build it the usual way:

.. code-block:: bash

    $ git clone git://github.com/30loops/thirty-cli.git
    $ python setup.py install

Creating an application
=======================

.. note::

    You have to specify your account name, username and password in order to
    use the client. You can do this either on the command line as arguments or
    by creating a ``.thirty.cfg`` in your home directory. See
    :ref:`thirty-client-global-options` and
    :ref:`thirty-client-configuration-file` for more information. For the rest
    of the document we assume you created yourself a configuration file to
    store your credentials.

Create an app with the following command:

.. code-block:: bash

    $ thirty create app <repository_location>

Replace ``repository_location`` with the URL to your code repository. At the
moment only Git repositories are supported. Every command has its own help
function:

.. code-block:: bash

    $ thirty help create app

This will show help for the ``create app`` subcommand. In this quickstart we
will deploy a simple cherrypy application. So our command looks like:

.. code-block:: bash

    $ thirty create app git://github.com/30loops/cherrypy-on-30loops.git

This will automatically create an app named ``cherrypyonloops`` and a
repository named ``cherrypyonloops``.

.. note:

    You can specify the name for the app by using the ``--name`` flag. If the
    flag is not specified the name will be determined by the name of the
    repository.

To see the configuration of the newly created app, use the following command:

.. code-block:: bash

    $ thirty show app cherrypyonloops

It will output something like:

.. code-block:: bash

    name: cherrypyonloops
    variant: python
    label: app
    region: ams1
    repo_branch: master
    instances: 1
    repo_commit: HEAD
    dns_record: 30loops-app-cherrypyonloops.30loops.net
    repository
        name: cherrypyonloops
        variant: git
        label: repository
        location: git://github.com/30loops/cherrypy-on-30loops.git
    database
        name: 30loops-db-cherrypyonloops
        variant: postgresql
        label: database
        username: 30loops-db-cherrypyonloops
        host: 192.168.0.53
        password: YzIyYTZjOWI2
        port: 9999

The app resource is now configured.

We will continue with deploying the newly created application.

Deploying an application
========================

Deploying an application is quite simple and fast, just run the following
command:

.. code-block:: bash

    $ thirty deploy cherrypyonloops

This will start the deployment. The client starts polling the logbook
immediately. You can also access the logbook manually by running:

.. code-block:: bash

    $ thirty logbook UUID

Where UUID is the ID of the deployment task.

After a succesfull deploy, your application will be availabl on the specified
DNS record: ``http://30loops-app-cherrypyonloops.30loops.net``.

Guides
======

To continue, you should read the indepth :doc:`30loops platform guide <guide>`.
We created a few guides with some sample applications. You can find examples
for a lot of different applications and stacks on https://30loops.github.com/

Django
------
- :doc:`Django CMS <django>`

WSGI
----
- :doc:`Simple WSGI app <wsgi>`

Additional support
==================

If you have any questions, please log in on http://help.30loops.net and
submit a ticket. You can also chat with us on #30loops at irc.freenode.net or
mail us at support@30loops.net.

.. _`pip website`: http://www.pip-installer.org/en/latest/requirements.html

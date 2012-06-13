================
Quickstart guide
================

.. note::

    It helps to first read the :doc:`firststeps to the 30loops platform
    <firststeps>` before following the quickstart.

This guide will provide some basic information about the platform and walk you
through the following steps:

#) Installing the 30loops client
#) Creating an application
#) Deploying an application

We will configure and deploy an example app you can find in our `sample apps on 
github`_. Its a very simple CherryPy application. It already contains a
``thirty.ini`` file, that configures the runtime environment. If you want to
deploy your own app, you have to provide your own ``thirty.ini`` file. The 
syntax is very simple, you can find more information at 
:ref:`runtime-configuration-label`.

.. _`sample apps on github`: https://30loops.github.com

Installing the 30loops client
=============================

Communicating with the 30loops platform can be done using the documented REST
api or using the 30loops client, called thirty. The REST api is documented
:doc:`here <rest_api>`. In this quickstart we will focus on using the client.
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

Creating an app
===============

.. note::

    You have to specify your account name, username and password in order to
    use the client. You can do this either on the command line as arguments or
    by creating a ``.thirty.cfg`` in your home directory. See
    :ref:`thirty-client-global-options` and
    :ref:`thirty-client-configuration-file` for more information. For the rest
    of the quickstart we assume you have created a configuration file with
    your credentials.

Create an app with the following command:

.. code-block:: bash

    $ thirty create <app> <repository_location>

Replace ``<app>`` with the name of your application. Replace
``repository_location`` with the URL to your code repository. At the moment
only Git repositories are supported. Every command has its own help function:

.. code-block:: bash

    $ thirty help create <app>

This will show help for the ``create app`` action. In this quickstart we
will deploy a simple cherrypy application. So our command looks like:

.. code-block:: bash

    $ thirty create cherryonloops git://github.com/30loops/cherrypy-on-30loops.git

This will create an app configuration named ``cherryonloops`` and a repository
configuration named ``cherryonloops``.

To see the configuration of the newly created app, use the following command:

.. code-block:: bash

    $ thirty show cherryonloops

It will output something like:

.. code-block:: bash

    name: cherryonloops
    variant: python
    region: ams1
    instances: 1
    repo_commit: HEAD
    dns_record: 30loops-app-cherryonloops.30loops.net
    repository
        name: cherryonloops
        variant: git
        location: git://github.com/30loops/cherrypy-on-30loops.git
    database
        name: 30loops-db-cherryonloops
        variant: postgres
        username: 30loops-db-cherryonloops
        host: not deployed
        password: OTYzMzgzZmNi
        port: not deployed

The app is now defined. We will continue with deploying the newly created app.

Deploying an app
================

.. note::

    The actual environment settings of your app is stored inside your
    repository, in a file called ``thirty.ini``. See
    :ref:`runtime-configuration-label` for more information.

Deploying an app is quite simple and fast, just run the following command:

.. code-block:: bash

    $ thirty deploy cherryonloops

This will start the deployment. Every action you run on your resources creates
a logbook. The command client starts polling the logbook immediately. You can
also access the logbook manually by running:

.. code-block:: bash

    $ thirty logbook UUID

Where UUID is the ID of the deployment task.

After a succesfull deploy, your application will be availabl on the specified
DNS record: ``http://30loops-app-cherrypyon30loops.30loops.net``.

Where to go
===========

To continue, you should read the indepth :doc:`30loops platform manual
<manual>`.  We created a few sample applications. You can find examples for a
lot of different applications and stacks on https://30loops.github.com/

Additional support
==================

If you have any questions, please log in on http://help.30loops.net and
submit a ticket. You can also chat with us on #30loops at irc.freenode.net or
mail us at support@30loops.net.

.. _`pip website`: http://www.pip-installer.org/en/latest/requirements.html

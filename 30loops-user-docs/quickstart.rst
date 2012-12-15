:tocdepth: 2

================
Quickstart guide
================

This quickstart guide will help to get up and running in no time. The first
part will walk you through an app creation and deploy, the second part will
discuss the first part and give more explanations.  We will configure and
deploy an example app you can find in our `sample apps on github`_. It's a very
simple CherryPy application. If you followed the short instructions right after
account registration, then the first part won't contain much new information.
You might want to skip right away to :ref:`part 2 <quickstart-part2>`.

.. _quickstart-part1:

Your first app
==============

Setting up the client and your account
--------------------------------------

Installing the ``thirty`` client is very simple:

.. code-block:: bash

    $ sudo pip install thirty-cli

For detailed instructions how to install the client see
:ref:`client-installation` for more information.

We configure your account by running the setup wizard of the client. You can
find :ref:`here <thirty-client-configuration-file>` more information.

.. code-block:: bash

    $ thirty setup

Creating an app
---------------

.. code-block:: bash

    $ thirty create quickstart git://github.com/30loops/cherrypy-on-30loops.git

This will create an app configuration named ``quickstart``. The app is now defined. We will continue
with deploying the newly created app.

Deploying an app
----------------

Deploying an app is quite simple and fast, just run the following command:

.. code-block:: bash

    $ thirty deploy quickstart

After a succesfull deploy, your application will be available on the specified
DNS record.

Your application is now up and running. To learn more what just happened, read
further.

.. _quickstart-part2:

Part 2: Some more explanations
==============================

Setting up the client and your account
--------------------------------------

Using the ``thirty`` client is currently the preferred way of using the 30loops
platform. Every interaction with the platform happens using our :doc:`HTTP API
<rest_api>`. You can use whatever tool you like to control your apps, even create
your own ones.  See :ref:`curl-examples-label` for examples how to use the
simple ``curl`` command to achieve the same results. If you come up with some
nice tool or way to control your apps, let us know.

You can always access the help function of the client:

.. code-block:: bash

    $ thirty help
    $ thirty help <command>

You can also look up the :doc:`detailed client documentation <client>`.

Creating an app
---------------

To host your own application on 30loops, you have to do 2 things:

#) Create a configuration for your application.
#) Deploy the application.

The first step has to happen only once at the beginning. Creating an app
configures it on our platform. You can configure different aspects of your app,
and configure which add on resources should be used. You can always update
your the configuration of your app later on. To create an app use the following
command:

.. code-block:: bash

    $ thirty create <app> <repository_location>

The name of your app and the repository location are the only required options.
There are more options, that are filled in with default values.  Replace
``<app>`` with the name of your application. Replace ``repository_location``
with the URL to your code repository. At the moment only Git repositories are
supported. You can find a :ref:`detailed description <client-create-label>` in
the client documentation.

To see the configuration of the newly created app, use the following command:

.. code-block:: bash

    $ thirty show quickstart

It will output something like:

.. code-block:: bash

    name: quickstart
    variant: python
    region: eu-nl
    published: false
    instances: 1
    repo_commit: HEAD
    dns_record: 30loops-app-quickstart.30loops.net
    repository
        name: quickstart
        variant: git
        location: git://github.com/30loops/cherrypy-on-30loops.git

Note that per default, no database gets created. If your application needs a
databse you should run the following command.

.. code-block:: bash

    $ thirty create quickstart.postgres

This will configure 30loops to provide your app with a PostgreSQL database. You can change
your configuration later using the ``update`` command. See the :ref:`client
documentation <client-update-label>` for mroe information on that.

At this moment, neither your application, nor your database really exist. Only
the its configuration. You have to deploy your application to actually
physically create it.

Deploying an app
----------------

Deploying your application is again quite easy.

.. code-block:: bash

    $ thirty deploy quickstart

This will start the deployment. The deployment will create a new app bundle
with your requirements, and pull the source code from your application. It will
further create any addon resource, like databases or mongodb instances, if they
don't exist yet.

The runtime of your application is described in a file, ``thirty.ini`` that is
part of your repository. It describes stuff like the root of your repository or
the wsgi entrypoint of your application. The ``quickstart`` example comes
with such a file already. You can find more information in :ref:`manual
<runtime-configuration-label>`. This is how the ``thirty.ini`` for this example
app looks like::

    [environment]
    root = .

    [wsgi]
    entrypoint = wsgi:application

The `sample apps on github`_ provide you more with examples.

Between deploys, only the source code gets updated. If you want to also create
a new bundle, you have to specify the ``-c`` option. You should do that, eg:
when your requirements change.

.. code-block:: bash

    $ thirty -c deploy quickstart

``deploy`` is a so called action. In contrary to ``create`` or ``show``,
``deploy`` manipulates teh physical aspect of your application. There are many
more actions available. Every action you run on your resources creates a
logbook. The API will return you a logbook id when you queue your action.  The
command client starts polling the logbook immediately. You can also access the
logbook manually by running:

.. code-block:: bash

    $ thirty logbook UUID

Where UUID is the ID of the deployment task. The logbook keeps you up to date
over what happens with your deploy and also tells you once it is finished.

At this point your app should be installed and accesible over the dns record,
that is provided to you. If you forgot the dns record, run a

.. code-block:: bash

    $ thrity show quickstart

to look it up again.

Where to go
===========

To continue, you should read the indepth :doc:`30loops platform manual
<manual>`.  We created a few sample applications. You can find examples for a
lot of different applications and stacks on https://30loops.github.com/

All your apps are created as free tier apps and have certain restrictions. If
you want to go live with your app read the section on :ref:`the free tier
<tier-label>`.

Additional support
==================

If you have any questions, please mail us at support@30loops.net. You can also 
chat with us on #30loops at irc.freenode.net. See you there!

.. _`sample apps on github`: https://30loops.github.com
.. _`pip website`: http://www.pip-installer.org/en/latest/requirements.html

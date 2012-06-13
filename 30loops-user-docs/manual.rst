=======================
30loops platform manual
=======================

Platform basics
===============

Working on the platform consists mainly of two tasks:

#) Creating, editing and deleting resources

   You can manipulate the configuration of your resources. This can be done by
   sending valid JSON messages to the API. To simplify this, you can
   generate the messages by using the :doc:`client`.

#) Queuing actions for a resource

   This manipulates the physical state of your resources. You can deploy or run
   commands in the context of your resource on the platform. Each resource
   accepts different actions. The ``thirty`` client supports all available
   actions. In the :doc:`REST API guide <rest_api>` the actions are explained
   in more detail.

Resources
---------

On 30loops, every service is called a resource. Examples of resources are
databases, applications and repositories. A resource is represented as a json
message, and each resource has several keys and values. The resources are
described in detail in the :doc:`REST API guide <rest_api>`.

A resource has at least the following fields:

**name**
  The name is a unique identifier. Each resource must have a unique name
  together with the label for this account, eg: You can have an app and a
  repository that both have the name ``blog``, but not two apps or two
  repositories.

**label**
  A resource has a label. This label describes the service. At this moment we
  support the following resource types:

  - app
  - repository
  - database

**variant**
  A resource can have a variant. That could be ``git`` or ``mercurial`` for
  repositories or ``python`` and ``static`` for apps.

.. _regions-label:

Regions
-------

Application layout
------------------

We tried to give you as much freedom as possible in setting up your repository
structure. To make a succesfull deploy we need to know a few things though.

You have to specify the project root. This is a relative path from the root of
your repository to where the actual project files are residing, eg: your django
project. Your project root gets added to the python path.

For example the following directory layout is possible::

    +--> setup.py
    +--> django_project
    |    +--> manage.py
    |    +--> urls.py
    |    +--> settings
    |    |    +--> __init__.py
    |    |    +--> production.py
    |    +--> templates
    +--> apps
         +--> blog
              +--> ..

You configure the project root among other things by supplying a runtime
configuration file named ``thirty.ini`` in the root of your repository. Like
that, eg: the appserver and the ``djangocmd`` and ``runcmd`` action, know which
directory hosts your actual project. See :ref:`runtime-configuration-label` for
more information.

The preferred way to install dependencies for your app is to supply a
requirements file. The location of this file is again configured in your
``thirty.ini`` file. But you can also write a ``setup.py`` for your app. You
can run any ``setup.py`` as part of the postinstall script. 

For WSGI apps this is similar::

    +--> src
         +--> myawesomeblog
              +--> __init__.py
              +--> app.py

By setting ``root`` in your ``thirty.ini`` to ``src/myawsomeblog/``, the right
directory gets added to the python path. Import paths like ``from
myawesomeblog.app import application`` are possible then.

.. _runtime-configuration-label:

``thirty.ini`` Runtime Configuration
------------------------------------

When you deploy an application, we will clone your repository and look for a
``thirty.ini`` file in your repository root directory. This file is used to
configure your runtime environment. We provide default values for almost all
configuration options. So most of the time this file will be very short. But
you can override any default we provide.

The format of this file is ``key = value`` and is organized in different
sections. This is an example config file.

.. code-block:: ini

    [environment]
    root = .

    [wsgi]
    entrypoint = wsgi:application

Currently this file can contain three different sections:

- **environment**: Configure the general python runtime environment.
- **wsgi**: Configure your generic wsgi application.
- **django**: Configure your django application.

Every app needs an ``environment`` section, and then depending on your app, you
have to define either a ``wsgi`` section or a ``django`` section.

``environment`` Section
-----------------------

In this section you configure your python environment. You have the following
options available:

**python_version** (default: python2.7)
  Choose the python version you want to use for your app. Currently only
  python2.7 is supported but we want to add support for python3 and pypy very
  soon.

**root** (default: .)
  You have to specify the root directory of your app relative to the root
  directory of your respository. If your repository looks like this::

    +--> setup.py
    +--> project      # This contains the root of your application.

  the root would look like this::

    root = project

  The default root directory of your project is ``.``, which is the root of the
  repository.

**requirements**
  Specify your requirements file as a relative to your repository root. If your
  repository looks like this::

    +--> setup.py
    +--> requirements.txt

  the option would be configured like this::

    requirements = requirements.txt

**Example**

.. code-block:: ini

    [environment]
    python_version = python2.7
    root = .
    requirements = requirements.txt

``wsgi`` Section
----------------

**wsgi**
  WSGI entrypoints have to be specified in the following format:
  ``python.module.path:callable``. If I have a repository structure like::

    +--> wsgiapp
         +--> __init__.py
         +--> main.py

  and ``main.py`` contains the callable ``app`` that serves as your WSGI entrypoint,
  the full entrypoint is expressed as ``wsgiapp.main:app``.

**Example**

.. code-block:: ini

    [wsgi]
    entrypoint = wsgiapp.main:app

``django`` Section
------------------

**settings** (default: settings)
  The python path to your settings file from your project root.

**inject_db** (default: False)
  Whether to inject the database configuration into your django settings. The
  injected database settings are placed at the end your settings file and
  therefore override any previous defined database settings. The template used
  looks like this::

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': '{{ db_name }}',
            'USER': '{{ db_user }}',
            'PASSWORD': '{{ db_password }}',
            'HOST': '{{ db_host }}',
            'PORT': '{{ db_port }}',
        }
    }

  If you want more control over your database settings, you should use
  :ref:`instance-environment-label` mechanism to write your settings.

**Example**

.. code-block:: ini

    [django]
    settings = settings.production
    inject_db = false

.. _instance-environment-label:

Environment Variables
---------------------

You can access the most important values of your environment inside of an
instance. There are two files, ``/app/conf/environment.conf`` and
``/app/conf/environment.json``. You can use them inside any shell script or
python script that you maybe want to run. For a shell script you can source the
``.conf`` file. You can read the json file in any python script and load the
string.

.. code-block:: bash

    $ cat /app/conf/environment.conf
    export VIRTUAL_ENV="/app/env"
    export STATIC_ROOT="/app/static"
    export MEDIA_ROOT="/app/media"
    export DB_PORT="9999"
    export PATH="/app/env/bin:/bin:/usr/bin"
    export DB_USER="30loops-app-thirtyblog"
    export DB_NAME="30loops-app-thirtyblog-production"
    export DB_HOST="pg.30loops.net"
    export DB_PASSWORD="ZjBmNDEyMWJj"
    export DJANGO_SETTINGS_MODULE="settings"
    export DJANGO_PROJECT_ROOT="thirtyblog"
    export MONGODB_NAME="30loops-monogdb-thirtyblog"
    export MONGODB_USER="30loops-monogdb-thirtyblog"
    export MONGODB_PASSWORD="DASDdsaw23DF"
    export MONGODB_HOST="192.168.0.99"
    export MONGODB_PORT="27701"

Add to your script the following line.

.. code-block:: sh

    #!/bin/bash
    ...
    source /app/conf/environment.conf
    ...
    echo $DB_PORT

.. code-block:: bash

    $ cat /app/conf/environment.json
    {
        {'VIRTUAL_ENV': '/app/env'},
        {'STATIC_ROOT': '/app/static'},
        {'MEDIA_ROOT': '/app/media'},
        {'DB_PORT': '9999'},
        {'PATH': '/app/env/bin:/bin:/usr/bin'},
        {'DB_USER': '30loops-app-thirtyblog'},
        {'DB_NAME': '30loops-app-thirtyblog-production'},
        {'DB_HOST': 'pg.30loops.net'},
        {'DB_PASSWORD': 'ZjBmNDEyMWJj'},
        {'DJANGO_SETTINGS_MODULE': 'settings'},
        {'DJANGO_PROJECT_ROOT': 'thirtyblog'},
        {'APP_USER': '30loops-app-thirtyblog'},
        {'MONGODB_NAME': '30loops-monogdb-thirtyblog'}
        {'MONGODB_USER': '30loops-monogdb-thirtyblog'}
        {'MONGODB_PASSWORD': 'DASDdsaw23DF'}
        {'MONGODB_HOST': '192.168.0.99'}
        {'MONGODB_PORT': '27701'}
    }

For your python application you can use something like:

.. code-block:: py

    import json
    with open('/app/conf/environment.json') as f:
        env = json.load(f)

    print env['DB_PORT']

Runtime environment
-------------------

The instances run on Ubuntu 12.04 with Python 2.7.3, and contain the following
installed python system packages::

    python-bcrypt 0.1-1build2
    python-bson 2.1-1
    python-cairo 1.8.8-1ubuntu3
    python-central 0.6.17
    python-crypto 2.4.1-1
    python-dateutil 1.5-1
    python-egenix-mxdatetime 3.2.1-1ubuntu1
    python-egenix-mxtools 3.2.1-1ubuntu1
    python-eventlet 0.9.16-1ubuntu4
    python-gdal 1.7.3-6ubuntu3
    python-gdata 2.0.14-2
    python-geoip 1.2.4-2ubuntu3
    python-gevent 0.13.6-1ubuntu1
    python-gi 3.2.0-3
    python-glade2 2.24.0-3
    python-gobject 3.2.0-3
    python-gobject-2 2.28.6-10
    python-greenlet 0.3.1-1ubuntu5
    python-gridfs 2.1-1
    python-gtk2 2.24.0-3
    python-imaging 1.1.7-4
    python-jinja2 2.6-1
    python-lxml 2.3.2-1
    python-m2crypto 0.21.1-2ubuntu2
    python-markupsafe 0.15-1
    python-matplotlib 1.1.0-1
    python-matplotlib-data 1.1.0-1
    python-minimal 2.7.2-9ubuntu6
    python-mysqldb 1.2.3-1build1
    python-nltk 2.0~b9-0ubuntu3
    python-numpy 1:1.6.1-6ubuntu1
    python-opencv 2.3.1-7
    python-pip 1.0-1build1
    python-pkg-resources 0.6.24-1ubuntu1
    python-psutil 0.4.1-1ubuntu1
    python-psycopg2 2.4.5-1
    python-pymongo 2.1-1
    python-pyparsing 1.5.2-2ubuntu1
    python-scipy 0.9.0+dfsg1-1ubuntu1
    python-setproctitle 1.0.1-1ubuntu1
    python-setuptools 0.6.24-1ubuntu1
    python-sqlalchemy 0.7.4-1
    python-sqlalchemy-ext 0.7.4-1
    python-support 1.0.14ubuntu2
    python-tk 2.7.3-1
    python-tz 2011k-0ubuntu5
    python-virtualenv 1.7-1
    python-yaml 3.10-2
    python-zmq 2.1.11-1

Static and Media files
----------------------

Static content are files like css or javascript. They get placed with every
deploy. Each instance has its own copies of those files. Media files are shared
among all instances and stored on a mass storage device. They are not changed
during a deploy and are meant for user generated content.

Paths to static and media files is handled per convention right now. The
webserver is configured to server static files from the path ``/static/`` and
media files from the path ``/media/``. The path locations on the instance are
``/app/static`` and ``/app/media`` respectively. You have to configure your
app accordingly if needed.

Postinstall hook
----------------

After each deploy the scripts ``postinstall`` and ``postinstall_all`` are
executed. The ``postinstall`` script runs only on the first created instance,
while the ``postinstall_all`` script runs on every instance.

The script needs to be in the root of your repository, and must be executable.
This script can be any language, just provide the right shebang:

For Python code:

.. code-block:: bash

    $ cat postinstall
    #!/usr/bin/env python
    run_some_function()

Or for example some BASH code:

.. code-block:: bash

    $ cat postinstall_all
    #!/bin/sh
    cp someimagefile /app/static

This would also be the correct place to run a syncdb after each deploy:

.. code-block:: bash

    #!/bin/sh
    python manage.py syncdb --noinput

.. note::

    The deployment process will fail if the script ends with an error return
    code!

Thirty client
=============

Installation
------------

To install the ``thirty-cli`` run:

.. code-block:: bash

    $ pip install -U thirty-cli

This should install all necessary requirements:

- python-docar
- libthirty
- requests
- argparse

If you don't have ``pip`` installed you can also use ``easy_install``:

.. code-block:: bash

    $ easy_install -U thirty-cli

Basics
------

The client is quite self-explaining. When you just type in ``thirty`` you will
get an overview of the various options. The basic structure of a command is:

.. code-block:: bash

    $ thirty <command> <subcommand> --flag1 somevariable --flag2 somevariable


Help on commands
----------------

You can get help of a function by running one of the following commands:

.. code-block:: bash

    $ thirty help <command>
    $ thirty help <command> <subcommand>

Each command has its own set of subcommands and flags.

Global Options
--------------

The ``thirty`` command line tool uses a few global options to set stuff like
authentication credentials or output formats. You can also omit them and
configure a `thirty.cfg Configuration File`_ to specify those values. Global
options specified on the command line take precedence over options specified in
the config file.

``-u, --username`` *<username>*
  Specify the username to use when authenticating a request to the API
  endpoints.

``-p, --password`` *<password>*
  Specify the password to use when authenticating a request to the API
  endpoints.

``-a, --account`` *<account>*
  Specify the account name when sending a request to the API endpoint.

``-r, --uri`` *<uri>*
  Specify the API URI to use for the request. The default API URI is
  ``https://api.30loops.net/``. You can override the default URI here. This is
  only useful for development purposes.

``-i, --api`` *<api>*
  Specify the default API version to use when making a request. The default is
  ``1.0``. You can override the default API version here.

``-R, --raw``
  Use a raw mode for printing output. The raw mode prints JSON messages as
  returned from the server, with out any indendation. This is handy if you want
  to use the ``thirty`` tool in scripts.

``thirty.cfg`` Configuration File
---------------------------------

You can create a configuration file in your home directory called
``.thirty.cfg``. Specify any global option there to save yourself the typing:

.. code-block:: bash

    $ cat ~/.thirty.cfg
    [thirtyloops]
    username = crito
    password = secret
    account = 30loops

The configuration file follows a simple INI style and collects all global
options under a section called ``[thirtyloops]``. Global options specified on
the command line take precedence over options specified in the config file.

Commands
--------

list
~~~~

.. code-block:: bash

    $ thirty list <label>

List all resources with the given label. Labels are written in plural, so the
followng commands are correct:

.. code-block:: bash

    $ thirty list apps
    $ thirty list repositories

**Example:**

.. code-block:: bash

    $ thirty list app
    thirtyloops
    djangocms

show
~~~~

.. code-block:: bash

    $ thirty show <label> <name>

Show the details of a resource.

**Example:**

.. code-block:: bash

    $ thirty show repository djangocms
    name: djangocms
    variant: git
    label: repository
    location: git://github.com/30loops/djangocms-on-30loops.git

create
~~~~~~
.. code-block:: bash

    $ thirty create <label>
    $ thirty create app [location]

Create a new resource. If you create an app, you have to specify a repository
location, or you have to specify and existing repository resource using the
``--repo`` flag. Each resource needs a name. If you omit the ``--name`` flag
when creating an app, it will use he respository name as its name.

.. code-block:: bash

    $ thirty create app https://github.com/30loops/djangocms.git

This will create two new resource. A repository resource with
``https://github.com/30loops/djangocms.git`` as location and ``djangocms``
as the name. It also creates an app resource, also with ``djangocms`` as name
and connecting the app to the before created repository.

This is a shortcut to

.. code-block:: bash

    $ thirty create respository --name djangocms https://github.com/30loops/djangocms.git
    $ thirty create app --name djangocms --repo djangocms

**flags**

``--name``
  Specify the name of the resource.

**app specific flags**

``--cname``
  Use this option if you use a custom domain. Create a CNAME record for your
  domain and point it to the default application name on 30loops (for example
  30loops-app-djangocms-production.30loops.net).

``--instances``
  The number of instances you want your app to deploy to. This defaults to one
  instance.

``--repo``
  The name of an existing app resource, you want to connect to this app. The
  app will checkout this repository during a deploy.

``--region``
  Specify in which region you want to run your application in. See the section
  about :ref:`regions-label` for more details.

``--create-db``
  As a default each app gets created with one database. If you set this value
  to false, the app gets created without a db.

**repository specific flags**

``--ssh-key``
  The path to a ssh key, that gets stored on the repository. Use this key for
  ssh key protected repositories.

update
~~~~~~
.. code-block:: bash

  $ thirty update <label> <name>

Update the details of a resource.

**Flags**

All flags of the create command are available. Additionally, these flags are
available on the ``update`` command:

delete
~~~~~~

.. code-block:: bash

    $ thirty delete <label> <name>

Delete a resource.

deploy
~~~~~~
.. code-block:: bash

    $ thirty deploy <app> --env <environment>

Deploy a specific app environment. It queues a new deployment of that
environment. See :doc:`REST API guide <rest_api>` for more information about
deploys.

runcmd
~~~~~~

.. code-block:: bash

    $ thirty runcmd <app> --env <environment> [<command> [<command> ...]]

Run a command in the context of your app environment. The full command is
specified enclosed by ``"``. The working directory of this command is the root
of your repository.

**Example:**

.. code-block:: bash

    $ thirty runcmd thirtyblog python init_db.py

**Options:**

``--occurence``
  Specifies on how many backends this command should be executed on. You can
  either specify a number or ``all``. Defaults to ``1``.

djangocmd
~~~~~~~~~

.. code-block:: bash

    $ thirty djangocmd <app> --env <environment> [<command> [<command> ...]

Run a django management command in the context of your django project. The full
command is specified enclosed by ``"``. The working directory of this command
is the root of your repository. You don't have to specify any settings module
or start the command with ``python manage.py``.

**Example:**

.. code-block:: bash

    $ thirty djangocmd thirtyblog --env development "syncdb"

**Options:**

``--occurence``
  Specifies on how many backends this command should be executed on. You can
  either specify a number or ``all``. Defaults to ``1``.

Cronjobs
========

Every instance runs cron by default. So you can easily create cronjobs to run on
one instance or on every instance. To do this, you need to create a cron file,
for example ``mycrontab``:

.. code-block:: bash

    $ cat mycrontab
    0 * * * * python myscript.py

To learn more about the format of the crontab file, see
http://en.wikipedia.org/wiki/Cron#Format.

To install the cronjob, you need to add a line to either ``postinstall`` or
``postinstall_all``, depending on if you want the cronjob to run a single
instance or on every instance. Example:

.. code-block:: bash

    $ cat postinstall
    #!/bin/sh
    crontab mycrontab

This will install the cron after deploying your application.

Running custom processes (unsupported!)
=======================================

It is possible to run your own custom processes. The processes will run as a
non-privileged user. To create a custom process, you need to add a ``.init/``
directory to your repository. In this ``.init/`` directory you need to create
an upstart file, that will be started after the deploy of an instance.

So the tree could look like:

.. code-block:: bash

    +--> .init
    |    +--> myprocess.conf
    +--> mycms
    |    +--> ..
    +--> requirements.txt
    +--> postinstall

The process file is an upstart configuration file. A very simple example:

.. code-block:: bash

    $ cat .init/myprocess.conf
    respawn

    exec /app/mycms/mycms/mycustomprocess

The process will not be started by default, so you need to add an additional
line to the ``postinstall`` script:

.. code-block:: bash

    $ cat postinstall
    #!/bin/sh
    crontab mycrontab
    start myprocess

For more information about upstart processes, read the Ubuntu Upstart Cookbook:
http://upstart.ubuntu.com/cookbook/.

Note: custom processes are completely unsupported!

Github examples
===============

On http://30loops.github.com we created a collection of sample apps and tutorials.
Please check it out, and let us know if you have recommendations for new apps!

.. include:: debugging.rst

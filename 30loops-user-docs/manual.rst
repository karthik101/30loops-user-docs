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
structure. To make a successful deploy we need to know a few things though.

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
====================================

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

``[environment]``
-----------------

In this section you configure your python environment. You have the following
options available:

**python_version** (default: python2.7)
  Choose the python version you want to use for your app. Currently only
  python2.7 is supported but we want to add support for python3 and pypy very
  soon.

**root** (default: .)
  You have to specify the root directory of your app relative to the root
  directory of your repository. If your repository looks like this::

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

  To use a requirements file for dependencies is the prefered way to install
  any 3rd party modules. But if you want to use a ``setup.py``, you can also do
  that. See :ref:`setup.py` for more information.

**systempackages** (unsupported!)
  Specify packages to be installed in your instances. The packages must be available
  in the standard Ubuntu Precise repositories.


**Example**

.. code-block:: ini

    [environment]
    python_version = python2.7
    root = .
    requirements = requirements.txt
    systempackages = memcached

``[wsgi]``
--------

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

``[django]``
------------

**settings** (default: settings)
  The python path to your settings file from your project root.

**Example**

.. code-block:: ini

    [django]
    settings = settings.production

``[app:processes]``
-------------------

The custom processes section can be used to run custom processes. To allow running
different processes on both the app instances and the worker instances, we 
splitted this in `[app:processes]` and `[worker:processes]`.

To define a process, simply supply a name and the command to run. We will take 
care of generating the configuration and piping stdout and stderr to the logging.

**Example**

.. code-block:: ini

    [app:processes]
    gunicorn = gunicorn_django graphite.settings


``[worker:processes]``
----------------------

The custom processes section can be used to run custom processes. To allow running
different processes on both the app instances and the worker instances, we 
splitted this in `[app:processes]` and `[worker:processes]`.

To define a process, simply supply a name and the command to run. We will take 
care of generating the configuration and piping stdout and stderr to the logging.

**Example**

.. code-block:: ini

    [worker:processes]
    carbon = python $PROJECT_ROOT/graphite/bin/carbon-cache.py --debug start


``[variables]``
---------------

This section can be used to define custom environment variables. This way you can
supply your S3 credentials or other app specific information to the instances.

**Example**

.. code-block:: ini

    [variables]
    PYTHONPATH = $PROJECT_ROOT/graphite:$PROJECT_ROOT/graphite/lib
    GRAPHITE_STORAGE_DIR = $HOME/data

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
    export LABEL="app"
    export PORT="800"
    export PATH="/app/env/bin:/bin:/usr/bin"
    export DATABASE_USER="30loops-database-thirtyblog"
    export DATABASE_NAME="30loops-database-thirtyblog"
    export DATABASE_HOST="pg.30loops.net"
    export DATABASE_PASSWORD="ZjBmNDEyMWJj"
    export DATABASE_URL="postgres://30loops-database-thirtyblog:ZjBmNDEyMWJj@192.168.0.53:9999/30loops-database-thirtyblog"
    export DJANGO_SETTINGS_MODULE="settings"
    export PROJECT_ROOT="thirtyblog"
    export DJANGO_ROOT="thirtyblog"
    export MONGODB_NAME="30loops-mongodb-thirtyblog"
    export MONGODB_USER="30loops-mongodb-thirtyblog"
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
        {'DATABASE_PORT': '9999'},
        {'LABEL': 'app'},
        {'PORT': '8000'},
        {'PATH': '/app/env/bin:/bin:/usr/bin'},
        {'DATABASE_USER': '30loops-app-thirtyblog'},
        {'DATABASE_NAME': '30loops-app-thirtyblog-production'},
        {'DATABASE_HOST': 'pg.30loops.net'},
        {'DATABASE_PASSWORD': 'ZjBmNDEyMWJj'},
        {'DATABASE_URL': 'postgres://30loops-database-thirtyblog:ZjBmNDEyMWJj@192.168.0.53:9999/30loops-database-thirtyblog'},
        {'DJANGO_SETTINGS_MODULE': 'settings'},
        {'PROJECT_ROOT': 'thirtyblog'},
        {'DJANGO_ROOT': 'thirtyblog'},
        {'APP_USER': '30loops-app-thirtyblog'},
        {'MONGODB_NAME': '30loops-mongodb-thirtyblog'}
        {'MONGODB_USER': '30loops-mongodb-thirtyblog'}
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

.. _`setup.py`:

``setup.py``
------------

If you use ``setup.py`` to install dependencies, you can do so in a
``postinstall_all`` hook. Its very easy, create in your repository root
a file called ``postinstall_all``, make it executable and add the following
lines to it:

.. code-block:: bash

    #!/bin/sh
    python setup.py install

.. note::

    Please note that we recommend you to use a requirements file to install
    your dependencies. It results in faster deploys than using a ``setup.py``.

We have an example django app, that uses a ``setup.py`` instead of a
requirements file in our `github repository`_.

.. _`github repository`: https://github.com/30loops/django-on-30loops

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

Running custom processes
========================

.. note::

    Currently we provide only limited support for running your own processes in
    this way.

The processes section in the `thirty.ini` configuration file can be used to run 
custom processes. To allow running different processes on both the app instances 
and the worker instances, we splitted this in:

``app:processes``

and 

``worker:processes``

To define a process, simply supply a name and the command to run. We will take 
care of generating the configuration and piping stdout and stderr to the logging.

**Example**

.. code-block:: ini

    [app:processes]
    gunicorn = gunicorn_django graphite.settings

    [worker:processes]
    carbon = python $PROJECT_ROOT/graphite/bin/carbon-cache.py --debug start

To get logs from the custom processes, you have to provide the process name to
the logs command:

.. code-block:: bash

    thirty logs myapplication --process mycustomprocess

Debugging your application
==========================

When deploying your application on 30loops, you might encounter some errors.
This guide will help you debug your application.

Logbook
-------

The logbook can help you debugging the deployment itself. If you deploy, the 
client will tail the logbook, and show any errors. If errors occur, most likely
there is also a description of the error, which will give you hints on how to
solve them.

If the logbook doesn't give enough information to fix the problem, you should
ask us to help you out.

Logs
----

The logs will help you debugging any errors in your application. This requires
a successful deploy, because logfiles are generated from active instances.

To show logs for an application, you can use the following command:

.. code-block:: bash

    $ thirty logs <app>

This will show the logs of `gunicorn` and `nginx` by default. If you need logs 
of a separate process, you can use the ``--process`` option:

.. code-block:: bash

    $ thirty logs <app> --process nginx

Currently we capture logs from `nginx`, `gunicorn` and `postgres`. To 
limit the number of returned log entries, use the ``--limit`` option.

Github examples
===============

On http://30loops.github.com we created a collection of sample apps and tutorials.
Please check it out, and let us know if you have recommendations for new apps!

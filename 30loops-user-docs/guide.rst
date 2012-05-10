==========================
30loops.net Platform Guide
==========================

App Project Structure
=====================

We tried to give you as much freedom as possible in setting up your repository
structure. To make a succesfull deploy we need to know a few things though.

You have to specify the project root. This is a relative path from the root of
your repository to where the actual project files are residing, eg: you django
project.

For example the following directory layout is possible::

    +--> thirty.ini
    +--> setup.py
    +--> requirements.txt
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
configuration file in the root of your repository. See
:ref:`runtime-configuration-label` for more information.

The preferred way to install dependencies for your app is to supply a
requirements file. The location of this file is again configured in your
``thirty.ini`` file. But you can also write a ``setup.py`` for your app.  You
can run any ``setup.py`` as part of the postinstall script. 

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

    root = projectA

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
    entrypoint = main:app

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

Instance Environment
====================

You can access the most important values of your environment inside of an
instance. There are two files, ``/app/conf/environment.conf`` and
``/app/conf/environment.json``. You can use them inside any shell script or
python script that you maybe want to run. For a shell script you can source the
``.conf`` file. You can read the json file in any python script and load the
string.

::

    cat /app/conf/environment.conf

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

Add to your script the following line.

.. code-block:: sh

    #!/bin/bash
    ...
    source /app/conf/environment.conf
    ...
    echo $DB_PORT

::

    cat /app/conf/environment.json

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
        {'APP_USER': '30loops-app-thirtyblog'}
    }

For your python script you can use something like that.

.. code-block:: py

    import json
    with open('/app/conf/environment.json') as f:
        env = json.load(f)

    print env['DB_PORT']

Database
========



Static and Media Files
======================

Static content are files like css or javascript. They get placed with every
deploy. Each instance has its own copies of those files. Media files are shared
among all instances and stored on a mass storage device. They are not changed
during a deploy and are meant for user generated content.

Paths to static and media files is handled per convention right now. The
webserver is configured to server static files from the path ``/static/`` and
media files from the path ``/media/``. The path locations on the instance are
``/app/static`` and ``/app/media`` respectively. You have to configure your
app accordingly if needed.

Web Stack
=========

Python Libraries
================

Post Installation script
========================

After each deploy the script ``postinstall`` gets executed. This script needs
to be in the root of your repository, and must be executable. This script can
be any language, just provide the right shebang:

For Python code:

.. code-block:: py

    #!/usr/bin/env python
    run_some_function()

Or for example some BASH code:

.. code-block:: bash

    #!/bin/sh
    cp someimagefile /app/static

This would also be the correct place to run a syncdb after each deploy:

.. code-block:: bash

    #!/bin/sh
    python manage.py syncdb --noinput

.. note::

    The postinstall command is ran on one instance only, to run a command on
    more instances you need to manually run a command using the client.

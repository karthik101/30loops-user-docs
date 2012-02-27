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

You configure ``django_project_root`` to ``django_project`` and enable
``install_setup_py`` by setting it to ``True``. The deploy runs a ``python
setup.py install`` to install your apps into the python path. And the appserver
and the ``djangocommand`` action know which directory hosts your actual
project. 

For WSGI apps this is similar::

    +--> src
         +--> myawesomeblog
              +--> __init__.py
              +--> app.py

By setting ``wsgi_project_root`` to ``src/myawsomeblog/``, the right directory
gets added to the python path. Import paths like ``from myawesomeblog.app
import application`` are possible then.

Django Apps
===========

Wsgi Apps
=========

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

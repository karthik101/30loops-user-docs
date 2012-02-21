==========================
30loops.net Platform Guide
==========================

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

Web Stack
=========

Python Libraries
================

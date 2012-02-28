===================
Django Flavor Guide
===================

You can host any `Django`_ application using the Django flavor. In this guide
we will install a typical django application and discuss all needed
configuration options.

We will install a Django-CMS application. You can find our django app in our
`example repository`_ on github.

Our repository looks like this::

    +--> requirements.txt
    +--> mycms
         +--> __init__.py
         +--> manage.py
         +--> production.py
         +--> settings.py
         +--> urls.py
         +--> templates

As you can see this is a very simple Django application, nothing fancy. We have
two settings files, ``settings.py`` is used for local development and contains
most settings and ``production.py`` is the settings file we use on the 30loops
platform. We define all our requirements in ``requirements.txt``.

So lets create our application and deploy it. First we create the app and then
an environment for it::

    $ thirty create app 30loops-cms

    {
        "environments": [],
        "name": "30loops-django-cms",
        "repository": {
            "location": "git@github.com:30loops/django-cms-30loops.git",
            "name": "30loops-django-cms",
            "variant": "git"
        },
        "variant": "python"
    }

    $ thirty create app 30loops-cms production

    {
        "backends": [{"region": "eu1", "count": 1}],
        "cname_records": [],
        "flavor": "django",
        "install_setup_py": false,
        "name": "production",
        "repo_branch": "master",
        "repo_commit": "HEAD",
        "requirements_file": "requirements.txt",
        "djangoflavor": {
            "inject_db": false,
            "django_project_root": "mycms",
            "django_settings_module": "production",
            "auto_syncdb": false
        }
    }

The Django flavor knows the following options:

``inject_db``
  Tells the server to automaticaly inject db settings when deploying. The db
  settings are injected at the end of the settings file you specify.

``django_project_root``
  The relative path to your django project folder. Thats the folder that
  contains your ``manage.py`` and most likely your ``urls.py``.

``django_settings_module``
  The python module path to your settings file. This has to be specified in a
  dotted syntax, eg: ``module.settings``.

.. _`Django`: http://djangoproject.com
.. _`example repository`: https://github.com/30loops/django-cms-30loops

Creating a Super User
=====================

To automatically create a superuser after the deploy, you need to use the 
``postinstall`` script. This is further explained in the Platform Guide. To 
create a superuser, create the following script:

``createadmin.py``

.. code-block:: py

  #!/usr/bin/env python
  from django.contrib.auth.models import User
  u, created = User.objects.get_or_create(username='admin')
  if created:
      u.set_password('password')
      u.is_superuser = True
      u.is_staff = True
      u.save()

``postinstall``

.. code-block:: bash

  #!/bin/bash
  python manage.py syncdb --noinput
  python createadmin.py

This will create a user ``admin`` with password ``password``. Of course, replace
these with the desired username and password. Remember to make the postinstall
script executable in your repository, and delete it from any public 
repositories!

=============================
Deploying Django applications
=============================

You can deploy any `Django`_ application using the Django flavor. In this guide
we will install a typical django application and discuss all the needed
configuration options in more detail.

The example application is a Django-CMS application. You can find our Django 
app in our `example repository`_ on github.

Our repository looks like this::

    +--> postinstall
    +--> requirements.txt
    +--> mycms
         +--> __init__.py
         +--> manage.py
         +--> production.py
         +--> settings.py
         +--> urls.py
         +--> templates

As you can see this is a simple Django application, nothing fancy. We have
two settings files, ``settings.py`` is used for local development and contains
most settings and ``production.py`` is the settings file we use on the 30loops
platform. We define all the requirements in ``requirements.txt``.

Commandline options
-------------------

For a list of common options, please see :doc:`client`.

**Django specific options**

``--inject-db``
  This tells the server to automaticaly inject the database settings during the
  deploy. The database settings are injected at the bottom of the settings file 
  you specified. By default, this option is set to ``true``.

``--django-settings-module``
  This is the python module path to your settings file. This has to be 
  specified in a dotted syntax, for example: ``module.settings``. By default
  this option is set to ``settings``.

.. _`Django`: http://djangoproject.com
.. _`example repository`: https://github.com/30loops/django-cms-30loops


Create a Django application
---------------------------

So lets create our application and deploy it. First we create the app and an
additional environment::

    $ thirty create app djangocms git://github.com/30loops/django-cms-30loops.git --flavor django --root mycms --settings settings
    App djangocms created!

    $ thirty create app 30loops-cms dev --root mycms --settings dev
    Environment dev created!

    $ thirty show app djangocms

        name: djangocms
        variant: python
        label: app
        repository
            name: djangocms
            variant: git
            label: repository
            location: git://github.com/bastichelaar/Django-CMS-30loops.git
        environments
          name: dev
            flavor: django
            requirements_file: requirements.txt
            project_root: mycms
            repo_branch: master
            install_setup_py: False
            repo_commit: HEAD
            database
                name: 30loops-app-djangocms-dev
                variant: postgresql
                label: database
                username:
                host: 
                password:
                port:
            djangoflavor
                inject_db: True
                django_settings_module: dev
            backends
                count: 1
                region: eu1
          name: production
            flavor: django
            requirements_file: requirements.txt
            project_root: mycms
            repo_branch: master
            install_setup_py: False
            repo_commit: HEAD
            database
                name: 30loops-app-djangocms-production
                variant: postgresql
                label: database
                username:
                host:
                password:
                port:
            djangoflavor
                inject_db: True
                django_settings_module: settings
            backends
                count: 1
                region: eu1

.. note::

    We left the database information out on purpose

As you can see, the application has been created with two environments, a
production environment and a development environment. Each environment has its
own database and settings, but they both are connected to the same application.
This means they share the same repository, that is connected to the application.
You can modify and deploy the environments independent from eachother.

To distinguish branches, use the options ``--repo-branch`` and ``--repo-commit``
when creating an environment.

Creating a Super User
=====================

To automatically create a superuser after the deploy, you can use a 
``postinstall`` script. This is further explained in more detail in the 
:doc:`Platform Guide <platform_guide>`. To create a superuser, create the 
following script:

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
script executable in your repository, and delete the createadmin.py from any 
public repositories!

Deploying the Django application
================================

To deploy the application, run::

  thirty deploy djangocms

This will deploy the djangocms production environment. To deploy the development
environment, run::

  thirty deploy djangocms --env dev

After executing the deploy command, the client will start polling the logbook.
This will look similar to this::

  $ thirty deploy wsgiapp dev

  Started deployment (logbook uuid: 8b932504-5e12-11e1-978ef-123b213121f)
  Creating a virtualenv for your application, this can take up to 150 seconds...
  Stage completed
  Creating database, this can take up to 10 seconds...
  Stage completed
  Requesting instances, this can take up to 100 seconds...
  Stage completed
  Configuring instances, this can take up to 40 seconds...
  Stage completed
  Adding the instances to the monitoring systems, this can take up to 10 seconds...
  Stage completed
  Reloading the loadbalancers, this can take up to 30 seconds...
  Stage completed
  Your application is successfully deployed on http://30loops-app-djangocms-dev.30loops.net

Your application will be available on the specified URL (and on any cnames you 
specified and pointed to this URL).

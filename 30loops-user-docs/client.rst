=============
Thirty client
=============

Installation
============

To install the ``thirty-cli`` run::

    pip install -U thirty-cli

This should install all necessary requirements:

- python-docar
- libthirty
- requests
- argparse

If you don't have ``pip`` installed you can also use ``easy_install``::

    easy_install -U thirty-cli

Usage
=====

::

    thirty [-u <username>] [-p <password>] [-a <account>] [-r <uri>]
           [-i <api>] [-R]
           <action> ...

Getting help
------------

This document gives an overview of the available flags when creating or updating
and application. The client also has an inline help function::

  thirty help <command>

For help on a subcommand use::

  thirty help <command> <subcommand>

.. _thirty-client-global-options:

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
  ``https://api.30loops.net/``. You can override the default URI here.

``-i, --api`` *<api>*
  Specify the default API version to use when making a request. The default is
  ``1.0``. You can override the default API version here.

``-R, --raw``
  Use a raw mode for printing output. The raw mode prints JSON messages as
  returned from the server, with out any indendation. This is handy if you want
  to use the ``thirty`` tool in scripts.

.. _thirty-client-configuration-file:

``thirty.cfg`` Configuration File
---------------------------------

You can create a configuration file in your home directory called
``.thirty.cfg``. Specify any global option there to save yourself the typing::

    cat ~/.thirty.cfg
    [thirtyloops]
    username = crito
    password = secret
    account = 30loops

The configuration file follows a simple INI style and collects all global
options under a section called ``[thirtyloops]``. Global options specified on
the command line take precedence over options specified in the config file.

list
----

::

    thirty list <label>

List all resources with the given label.

**Example:**

::

    $ thirty list app
    thirtyloops
    djangocms

show
----

::

    thirty show <resource> <name> [environment]

Show the details of a resource. If ``[environment]`` is given it will show the
details of a specific app environment instead of the app itself.

**Example:**

::

    $ thirty show repository djangocms
    name: djangocms
    variant: git
    label: repository
    location: git://github.com/bastichelaar/Django-CMS-30loops.git

create
------
::

    thirty create <label> <name> [location]

Create a new resource. Each resource has its own set of flags. Note that
database resources cannot be created manually, but will be created when
creating an application environment.

**Required arguments**

``<label>``
  The label defines the type of the resource. This can be ``app``,
  ``repository`` or ``environment``.

``<name>``
  The name you give the resource

**flags**

``--root``
  This flag specifies where the root of your application is. By default this is
  set to the most upper directory.

``--flavor``
  The flavor flag needs to be set for every application. Currently we have the
  ``wsgi`` flavor and ``django`` flavor.

``--cname``
  Use this option if you use a custom domain. Create a CNAME record for your
  domain and point it to the default application name on 30loops (for example
  30loops-app-djangocms-production.30loops.net).

``--environment``
  By default, the created environment will be named ``production``. You can
  override this by specifying a custon environment name.

``--requirements``
  This option specifies the file to use for the pip install command. By default
  this is set to ``requirements.txt``.

``--install-setup-py``
  This flag enables or disables the ``python setup.py install`` command. If you
  need to run this on deployment, please set it to ``true``. Default is
  ``false``.

``--backends``
  This flag specifies the number of backends to deploy on. By default it is set
  to 1.

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


**WSGI specific options**

``--wsgi-entrypoint``
  This flag specifies the entrypoint of your application. Each incoming
  request will be routed to this function. WSGI entrypoints have to be specified
  in the following format: ``python.module.path:callable``, for example
  ``wsgiapp.main:application``.

update
------

::

    thirty update <lable> <resource_name> [environment]

Update the details of a resource. If ``[environment]`` is given it will update the
details of a specific app environment instead of the app itself.

**Flags**

All flags of the create command are available. Additionally, these flags are
available on the ``update`` command:

``--repo-branch``
  This option specifies which branch of the repository to fetch. By default this
  is set to ``master``.

``--repo-commit``
  This option specifies which commit of the repository to fetch. By default this
  is set to ``HEAD``.

``--add-cname``
  This flag adds an additional CNAME to the environment.

``--del-cname``
  This flag deletes a CNAME from the environment.

delete
------

::

    thirty delete <lable> <resource_name> [environment]

Delete a resource. If ``[environment]`` is given it will delete the app
environment instead of the app itself.

deploy
------

::

    thirty deploy <app> <environment>

Deploy a specific app environment. It queues a new deployment of that
environment. See :doc:`REST API guide <rest_api>` for more information about
deploys.

runcmd
------

::

    thirty runcmd <app> <environment> "<command>"

Run a command in the context of your app environment. The full command is
specified enclosed by ``"``. The working directory of this command is the root
of your repository.

**Example:**

::

    thirty runcmd thirtyblog production "python init_db.py"

**Options:**

``--occurence``
  Specifies on how many backends this command should be executed on. You can
  either specify a number or ``all``. Defaults to ``1``.

djangocmd
---------

::

    thirty djangocmd <app> <environment> "<management command>"

Run a django management command in the context of your django project. The full
command is specified enclosed by ``"``. The working directory of this command
is the root of your repository. You don't have to specify any settings module
or start the command with ``python manage.py``.

**Example:**

::

    thirty djangocmd thirtyblog production "syncdb"

**Options:**

``--occurence``
  Specifies on how many backends this command should be executed on. You can
  either specify a number or ``all``. Defaults to ``1``.

logs
----

::

    thirty logs <app>

Shows the logs of your application. All logs are collected centrally, so you
can get aggregated logs of all instances.

**Example:**

::

    thirty logs thirtyblog --process nginx,gunicorn --limit 20

**Options:**

``--environment``
  Specifies the environment of the application

``--process``
  A comma separated list of the processes to fetch the logs from. Currently
  only ``nginx``, ``gunicorn`` and ``postgres`` are available. Notice that
  ``postgres`` logs can only be fetched separately.

``--limit``
  Limit of the entries to fetch. By default this is set to 10.

logbook
-------

::

    thirty logbook <uuid>

Shows the logbook of an action, for example a deploy. The output is valid JSON.

**Example:**

::
    thirty logbook e6418181-5b3f-483b-a1c5-c88a55f0550a

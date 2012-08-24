=============
Thirty client
=============

.. _`client-installation`:

Installing the 30loops client
=============================

Communicating with the 30loops platform can be done using the documented REST
api or using the 30loops client, called thirty. The REST api is documented
:doc:`here <rest_api>`. You can install the client using pip:

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

Getting help
============

The client provides a help command. You can query the help by typing:

.. code-block:: bash

    $ thirty help

To get the help for a specific action or an action target, type:

.. code-block:: bash

    $ thirty help <action>
    $ thirty help <action> <resource>

.. _thirty-client-global-options:


Global Options
==============

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

``-i, --api`` *<api>*
  Specify the default API version to use when making a request. The default is
  ``0.9``. You can override the default API version here.

``-R, --raw``
  Use a raw mode for printing output. The raw mode prints JSON messages as
  returned from the server, with out any indentation. This is handy if you want
  to use the ``thirty`` tool in scripts.

.. _thirty-client-configuration-file:

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

You can run ``thirty setup``, to create the initial configuration file. A
simple wizard will help you.

Actions
=======

setup
-----

::

    thirty setup

Setup the initial configuration file. If a file already exists, the setup
wizard will not overwrite the existing file.

**Example:**

::

    $ thirty setup

    Please enter your accountname: 30loops
    Please enter your username: crito
    Password:
    The configuration file has been created. You can now use the client.

list
----

::

    thirty list

List all of your apps. It lists all apps, and each resource associated to a
resource.

**Example:**

::

    $ thirty list

    cherryon30loops
        repository: cherryon30loops
        database: 30loops-db-cherryon30loops
    website
        repository: website
        database: 30loops-database-website

show
----

::

    thirty show <app>

Show the details of an app. The app is identified by its name. It also shows
the details of all resources associated to this app.

**Example:**

::

    $ thirty show cherryon30loops

    name: cherryon30loops
    variant: python
    region: ams1
    instances: 1
    published: False
    repo_commit: HEAD
    dns_record: 30loops-app-cherryon30loops.30loops.net
    repository
        name: cherryon30loops
        variant: git
        location: git://github.com/30loops/cherrypy-on-30loops.git
    database
        name: 30loops-db-cherryon30loops
        variant: postgres
        username: 30loops-db-cherryon30loops
        host: 192.168.0.53
        password: MWRjZWViY2Rk
        port: 9999

.. _client-create-label:

create
------

::

    thirty create <resource>

Create a new resource. ``<resource>`` can be one of the following arguments:

create ``<app>``
~~~~~~~~~~~~~~~~

::

    thirty create <app> [--cname CNAME] [--repository REPOSITORY]
                         [--region REGION] [--instances INSTANCES] [--no-db]
                         [--variant VARIANT]
                         <location>

Create a new app.

**Example**

.. code-block:: bash

    $ thirty create cherryon30loops git://github.com/30loops/cherrypy-on-30loops.git

**Required Arguments**

``<location>``
  This is the URI of the repository that will be used for this app. You have to
  specify at app creation a repository location.

**Optional Arguments**

``--cname CNAME``
  Connect a CNAME record to this app. Specify multiple times if needed.

``--repository REPOSITORY``
  Specify an existing repository to connect to this app. You reference
  repositories by their name. If you want to use this option, as a current
  limitation, you still have to specify a location.

``--region REGION``
  The region of this app (defaults to ams1).

``--instances INSTANCES``
  The number of instances to deploy your app on. Each app gets configured with
  one instance as a default.

``--no-db``
  Don't create a database for this app. As a default each app gets created
  already with a database. Use this option if you don't need a database, eg for
  static apps.

``--variant VARIANT``
  The variant of this app (default: python).

create ``<app>.repository``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    thirty create <app>.repository [--name <name>] [--ssh-key SSH_KEY]
                                    <location>

Create a new repository and attach it to <app>

**Example**

.. code-block:: bash

    $ thirty create cherryon30loops.repository git://github.com/30loops/cherrypy-on-30loops.git --name cherrypyon30loops

**Required Arguments**

``<location>``
  URI of the repository location.

**Optional Arguments**

``--name <name>``
  Custom name of the repository resource (will be generated automatically from
  the repository URI otherwise).

``--ssh-key SSH_KEY``
  SSH key (password-less) for a SSH protected repository. The full path to the
  key file must be provided.

create ``<app>.database``
~~~~~~~~~~~~~~~~~~~~~~~~~

**Example**

.. code-block:: bash

    $ thirty create <app>.database

Create a new database resource for this app. No arguments are required.

create ``<app>.worker``
~~~~~~~~~~~~~~~~~~~~~~~

::

    thirty create <app>.worker [--instances INSTANCES]

Create a new worker.

**Example**

.. code-block:: bash

    $ thirty create <app>.worker

**Optional Arguments**

``--instances INSTANCES``
  The number of worker instances to deploy. Defaults to one instance.

create ``<app>.mongodb``
~~~~~~~~~~~~~~~~~~~~~~~~

**Example**

.. code-block:: bash

    $ thirty create <app>.mongodb

Create a MongoDB database for this app. No arguments are required

.. _client-update-label:

update
------

::

    thirty update <resource>

Update an existing resource.

update ``<app>``
~~~~~~~~~~~~~~~~

::

    thirty update <app> [--add-cname ADD_CNAME] [--del-cname DEL_CNAME]
                        [--instances INSTANCES] [--repository REPOSITORY]
                        [--repo-commit REPO_COMMIT] [--add-var ADD_VAR]
                        [--del-var DEL_VAR]


**Example**

.. code-block:: bash

    $ thirty update cherryon30loops --add-cname www.example.org

**Optional Arguments**

``--add-cname ADD_CNAME``
  Add an additional CNAME to the app.

``--del-cname DEL_CNAME``
  Remove a CNAME from the app.

``--instances INSTANCES``
  The number of instances to deploy your app on. Note that only the
  configuration will be updated. for the new instance count to take effect, you
  still have to run a `deploy`_. You can also use the `scale`_ command to
  immediately scale the number of instances for this app.

``--repository REPOSITORY``
  Change the repository to use for this app.

``--repo-commit REPO_COMMIT``
  Commit or branch of the repository to clone.

``--add-var ADD_VAR``
  Add a new environment variable to your application. Specify the variable in
  this format: ``VARIABLE=VALUE``. Those values are accesible inside your
  applications environment. Note that you can also specify environment variables
  in your ``thirty.ini`` file. If you dont wanna store sensitive values in a
  public repository, use this mechanism. Otherwise prefer the ``thirty.ini``
  over this method.

``--del-var DEL_VAR``
  Delete an environment variable from your app.

update ``<app>.repository``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    thirty update <app>.repository [--name <repository>]
                                    [--location LOCATION] [--ssh-key KEY]

Update the configuration of a repository.

**Example**

.. code-block:: bash

    $ thirty update cherryon30loops.repository --key ~/new_key.pub

**Optional Arguments**

``--name <repository>``
  Name of the repository to update (if not specified, <app>  will be used).

``--location LOCATION``
  Update URI of the repository.

``--ssh-key KEY``
  SSH key for a non-public repository (specify full path).

update ``<app>.worker``
~~~~~~~~~~~~~~~~~~~~~~~

::

    thirty update <app>.worker [--instances INSTANCES] [--add-var ADD_VAR]
                               [--del-var DEL_VAR]


Update the configuration of a worker.

**Example**

.. code-block:: bash

    $ thirty update cherryon30loops.worker --instances 3

**Optional Arguments**

``--instances INSTANCES``
  The number of worker instances to deploy. Note that this only changes the
  configuration of the worker. For this setting to take effect, you need to
  deploy the worker again. Or you use the `scale`_ command that immediately
  scales the worker.

``--add-var ADD_VAR``
  Add a new environment variable to your worker. Specify the variable in
  this format: ``VARIABLE=VALUE``. Those values are accesible inside your
  workers environment. Note that you can also specify environment variables
  in your ``thirty.ini`` file. If you dont wanna store sensitive values in a
  public repository, use this mechanism. Otherwise prefer ``thirty.ini``
  over this method.

``--del-var DEL_VAR``
  Delete an environment variable from your worker.

delete
------

::

    thirty delete <resource>

Delete a resource. ``<resource>`` can be one of the following:

- ``<app>``: Delete an app.
- ``<app>.database``: Delete a database.
- ``<app>.mongodb``" Delete a mongodb.
- ``<app>.repository``: Delete a repository.
- ``<app>.worker``: Delete a worker.

This command takes no further arguments.

deploy
------

::

    thirty deploy [--clean] <app>

Deploy an app. A regular deploy only pulls the latest code, but reuses the same
virtualenv for your app. if you want to create a clean virtualenv or update any
requirements, you have to make a clean deploy.

**Example**

.. code-block:: bash

    $ thirty deploy -c cherryon30loops

**Optional Arguments**

``--clean, -c``
  Perform a clean deploy. This rebuilds the virtualenv during the deploy. This
  takes longer than a normal deploy.

.. _publish-client-action:

publish
-------

::

    thirty publish <app>

Publish an app. By default apps are created as free tier apps. Several
restrictions apply on those apps. To go live with an app, you have to publish
it. This removes any restrictions set due to the free tier. See
:ref:`tier-label` for more information about free tier restrictions.

**Example**

.. code-block:: bash

    $ thirty publish cherryon30loops

runcmd
------

::

    thirty runcmd <resource>

Run a command in the context of your app or worker instances. The working
directory of this command is the root of your repository.

runcmd ``<app>``
~~~~~~~~~~~~~~~~

::

    thirty runcmd <app> [--occurrence OCCURRENCE] <command>

Run a generic command on one or more app instances.

**Required Arguments**

``<command>``
  Command to run.

**Optional Arguments**

``--occurrence OCCURRENCE``
  Number of app instances to run the command on (use "all" for all instances).

runcmd ``<app>.worker``
~~~~~~~~~~~~~~~~~~~~~~~

::

    thirty runcmd <app> [--occurrence OCCURRENCE] <command>

Run a generic command on one or more worker instances.

**Required Arguments**

``<command>``
  Command to run.

**Optional Arguments**

``--occurrence OCCURRENCE``
  Number of worker instances to run the command on (use "all" for all instances).

djangocmd
---------

::

    thirty djangocmd <resource>

Run a django management in the context of your app or worker instances. The
working directory of this command is the root of your repository. using a
`djangocmd`` is equivalent to using ``runcmd`` and specifying ``python
manage.py`` and a ``--settings`` argument in the command. ``djangocmd`` will
always use the settings path you specified in the environment file.

**Example**

.. code-block:: bash

    $ thirty djangocmd cherryon30loops syncdb

is equivalent to

.. code-block:: bash

    $ thirty runcmd cherryon30loops python manage.py syncdb --settings settings

djangocmd ``<app>``
~~~~~~~~~~~~~~~~~~~

::

    thirty djangocmd <app> [--occurrence OCCURRENCE] <command>

Run a django management command on one or more app instances.

**Required Arguments**

``<command>``
  Command to run.

**Optional Arguments**

``--occurrence OCCURRENCE``
  Number of app instances to run the command on (use "all" for all instances).

djangocmd ``<app>.worker``
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    thirty djangocmd <app> [--occurrence OCCURRENCE] <command>

Run a django management command on one or more worker instances.

**Required Arguments**

``<command>``
  Command to run.

**Optional Arguments**

``--occurrence OCCURRENCE``
  Number of worker instances to run the command on (use "all" for all instances).

scale
-----

::

    thirty scale <resource>

Scale a resource. This increases the configured instance count for this
resource and applies right away the physical changes. To pause a resource, you
can scale the resource to 0 instances.

scale ``<app>``
~~~~~~~~~~~~~~~

::

    thirty scale <app> <instances>

Scale the number of app instances.

**Example**

.. code-block:: bash

    $ thirty scale cherryon30loops 4

**Required Arguments**

``<instances>``
  Number of app instances to scale to. This is the final number of <app>
  instances.

scale ``<app>.worker``
~~~~~~~~~~~~~~~~~~~~~~

::

    thirty scale <app>.worker <instances>

Scale the number of worker instances.

**Example**

.. code-block:: bash

    $ thirty scale cherryon30loops.worker 0

**Required Arguments**

``<instances>``
  Number of worker instances to scale to. This is the final number of <app>
  instances.

restore
-------

::

    thirty restore <app>.database <location>

Restores a database from a specified URL. The current database will be deleted,
and a new database will be created and restored from the specified database 
dump.

The command we use internally to restore the database is:

.. code-block:: bash

    pg_restore --clean --no-acl --no-owner -d <database>

To make sure the database is restored correctly, you should dump your database
with the following command:

.. code-block:: bash

    pg_dump -Fc --no-acl --no-owner <database> > <dumpfile>

**Example:**

.. code-block:: bash

    thirty restoredb cherrypyon30loops http://mywebpage.com/database.dump

**Required Arguments:**

``<location>``
  The location of the database dump file.

restart
-------

::

    thirty restart <resource>

Restart all running process for your resource.

restart ``<app>``
~~~~~~~~~~~~~~~~~

::

    thirty restart <app>

Restart all app processes.

restart ``<app>.worker``
~~~~~~~~~~~~~~~~~~~~~~~~

::

    thirty restart <app>.worker

Restart all worker processes.

logs
----

::

    thirty logs [--process PROCESS] [--limit LIMIT] <app>

Shows the logs of your application. All logs are collected centrally, so you
can get aggregated logs of all instances.

**Example:**

.. code-block:: bash

    thirty logs thirtyblog --process nginx,gunicorn --limit 20

**Required Arguments:**

``<app>``
  The name of the app.

**Optional Arguments:**

``--process PROCESS``
  Specify the process to get the logs from. You can specify several processes
  by separating them with a comma (``,``) and no space in between. Currently
  the following processes can be selected:

  - nginx
  - gunicorn
  - postgresql

  (default: gunicorn,nginx)

``--limit LIMIT``
  The number of entries to return (default: 10).

logbook
-------

::

    thirty logbook <uuid>

Shows the logbook of an action, for example a deploy.. You see the uuid in then
you queue the action with client, or in the ``Location`` header of the HTTP
response, when talking to the API directly.

**Example:**

::
    thirty logbook e6418181-5b3f-483b-a1c5-c88a55f0550a

**Required Arguments:**

``<uuid>``
  The UUID of the logbook.

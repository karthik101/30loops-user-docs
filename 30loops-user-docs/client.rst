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
  returned from the server, with out any indendation. This is handy if you want
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

Actions
=======

list
----

::

    thirty list

List all of your apps. It lists all apps, and each resource associated to ai
resource.

**Example:**

::

    $ thirty list

    cherryonloops
        repository: cherryonloops
        database: 30loops-db-cherryonloops
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

    $ thirty show cherryonloops

    name: cherryonloops
    variant: python
    region: ams1
    instances: 1
    repo_commit: HEAD
    dns_record: 30loops-app-cherryonloops.30loops.net
    repository
        name: cherryonloops
        variant: git
        location: git://github.com/30loops/cherrypy-on-30loops.git
    database
        name: 30loops-db-cherryonloops
        variant: postgres
        username: 30loops-db-cherryonloops
        host: 192.168.0.53
        password: MWRjZWViY2Rk
        port: 9999

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

    $ thirty create cherryonloops git://github.com/30loops/cherrypy-on-30loops.git

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
  allready with a database. Use this option if you dont need a database, eg for
  static apps.

``--variant VARIANT``
  The variant of this app (default: python).

create ``<app>.repository``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    thirty create <app>.repository [--name <name>] [--ssh-key SSH_KEY]
                                    <location>

Create a new repository and attch it to <app>

**Example**

.. code-block:: bash

    $ thirty create cherryonloops.repository git://github.com/30loops/cherrypy-on-30loops.git --name cherrypyon30loops

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

update
------

::

    thirty update <resource>

Update an existing resource.

update ``<app>``
~~~~~~~~~~~~~~~~

::

    thirty update <app> [--add-cname ADD_CNAME] [--del-cname DEL_CNAME]
                         [--instances INSTANCES] [--region REGION]
                         [--repository REPOSITORY] [--repo-commit REPO_COMMIT]


**Example**

.. code-block::

    $ thirty update cherryonloops --add-cname www.example.org

**Optional Arguments**

``--add-cname ADD_CNAME``
  Add an additional CNAME to the app.

``--del-cname DEL_CNAME``
  Remove a CNAME from the app.

``--instances INSTANCES``
  The number of instances to deploy your app on. Note that only the
  configuration will be updated. for the new instance count to take effect, you
  still have to run a `deploy`_. You can also use the `scale`_ command to
  immediately sclae the number of instances for this app.

``--repository REPOSITORY``
  Change the repository to use for this app.

``--repo-commit REPO_COMMIT``
  Commit or branch of the repository to clone.

update ``<app>.repository``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    thirty update <app>.repository [--name <repository>]
                                    [--location LOCATION] [--ssh-key KEY]

Update the configuration of a repository.

**Example**

.. code-block::

    $ thirty update cherryonloops.repository --key ~/new_key.pub

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

    thirty update <app>.worker --instances INSTANCES

Update the configuration of a worker.

**Example**

.. code-block:: bash

    $ thirty update cherryonloops.worker --instances 3

**Optional Arguments**

``--instances INSTANCES``
  The number of worker instances to deploy. Note that this only changes the
  configuration of the worker. For this setting to take effect, you need to
  deploy the worker again. Or you use the `scale`_ command that immediately
  scales the worker.

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

scale
-----

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

==============
``thirty-cli``
==============

You can use the ``thirty-cli`` client tool to operate the 30loops platform. It
provides a text based interface to your resources and you can queue actions.
The client is not doing much more than helping you in crafting correct JSON
messages as described in the :doc:`REST API guide <rest_api>`. You need the
``EDITOR`` environment variable defined in your shell::

    export EDITOR='/usr/bin/vim'

Whenever you create or update resources, it will open your default editor and
already give you a template for the JSON message you have to edit. If you
create a new resource it will scaffold a template, and if you update an
existing resource your editor will contain the current representation of your
resource.

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
           <subcommand> ...

Getting Help
------------

To get the commands help output type::

    thirty help

To get help on a specific command type::

    thirty help <command>

Global Options
--------------

The ``thirty`` command line tool uses a few global options to set stuff like
authentication credentials or output formats. You can also omit them and
configure a `thirty.cfg Configuration File`_ to specify those values. Global
options specified on the command line take precedence over options specified in
the config file.

-u, --username *<username>*
  Specify the username to use when authenticating a request to the API
  endpoints.

-p, --password *<password>*
  Specify the password to use when authenticating a request to the API
  endpoints.

-a, --account *<account>*
  Specify the account name when sending a request to the API endpoint.

-r, --uri *<uri>*
  Specify the API URI to use for the request. The default API URI is
  ``https://api.30loops.net/``. You can override the default URI here.

-i, --api *<api>* (string)
  Specify the default API version to use when making a request. The default is
  ``1.0``. You can override the default API version here.

-R, --raw
  Use a raw mode for printing output. The raw mode prints JSON messages as
  returned from the server, with out any indendation. This is handy if you want
  to use the ``thirty`` tool in scripts.

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

Subcommands
-----------

list
~~~~

::

    thirty list <label>

List all resources with the given label.

**Example:**

::

    thirty list app
    {
        "items": [
            {
                "href": "http://localhost:8000/1.0/30loops/app/thirtyloops/", 
                "name": "thirtyloops"
            }, 
            {
                "href": "http://localhost:8000/1.0/30loops/app/thirtyblog/", 
                "name": "thirtyblog"
            }, 
        ], 
        "link": {
            "href": "http://localhost:8000/1.0/30loops/app/", 
            "rel": "self"
        }

show
~~~~

::

    thirty show <lable> <resource_name> [environment]

Show the details of a resource. If ``[environment]`` is given it will show the
details of a specific app environment instead of the app itself.

**Example:**

::

    thirty show repository
    {
        "username": "crito", 
        "name": "thirtyloops", 
        "variant": "git", 
        "label": "repository", 
        "link": {
            "href": "http://localhost:8000/1.0/30loops/repository/thirtyloops/", 
            "rel": "self"
        }, 
        "location": "https://github.com/30loops/thirtyloops", 
        "password": "password"
    }

create
~~~~~~

::

    thirty create <lable> <resource_name> [environment]

Create a new resource. If ``[environment]`` is given it will create a new app
environment instead of the app itself. Not all resources can be created that
way. Database resources for example are created automatically when creating an
app environment.

update
~~~~~~

::

    thirty update <lable> <resource_name> [environment]

Update the details of a resource. If ``[environment]`` is given it will update the
details of a specific app environment instead of the app itself.

delete
~~~~~~

::

    thirty delete <lable> <resource_name> [environment]

Delete a resource. If ``[environment]`` is given it will delete the app
environement instead of the app itself.

deploy
~~~~~~

::

    thirty deploy <app> <environment>

Deploy a specific app environment. It queues a new deployment of that
environment. See :doc:`REST API guide <rest_api>` for more information about
deploys.

runcmd
~~~~~~

::

    thirty runcmd <app> <environment> "<command>"

Run a command in the context of your app environment. The full command is
specified enclosed by ``"``. The working directory of this command is the root
of your repository. 

**Example:**

::

    thirty runcmd thirtyblog production "python init_db.py"

djangocmd
~~~~~~~~~

::

    thirty djangocmd <app> <environment> "<management command>"

Run a django management command in the context of your django project. The full
command is specified enclosed by ``"``. The working directory of this command
is the root of your repository. You don't have to specify any settings module
or start the command with ``python manage.py``.

**Example:**

::

    thirty djangocmd thirtyblog production "syncdb"

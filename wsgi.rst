=================
WSGI Flavor Guide
=================

Using the WSGI flavor, you can deploy any python web application following the
`WSGI standard`_. This includes frameworks like Flask, web.py and others.  We 
offer special support for Django applications.

Let's create a very simple WSGI app. The app is available on our 
`example repository`_ on Github.

The structure of the repository looks like this::

    +--> wsgiapp
         +--> __init__.py
         +--> main.py

The code is a very basic example of a WSGI app. Edit ``wsgiapp/main.py`` and 
insert the following code.

.. code-block:: py

    def application(environ, start_response):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers)
        return ['Hello world!\n']

This function serves as an entrypoint for the app server. Each incoming 
request will be routed to this function. WSGI entrypoints have to be specified 
in the following format: ``python.module.path:callable``. In this example this 
is ``wsgiapp.main:application``.

So let's create the application and deploy it. First create the new app and 
create an environment:

::

    $ thirty create app wsgiapp

    {
        "environments": [],
        "name": "wsgiapp",
        "repository": {
            "location": "git://github.com/crito/wsgiapp.git",
            "name": "wsgiapp",
            "variant": "git"
        },
        "variant": "python"
    }

    $ thirty create app wsgiapp dev

    {
        "backends": [{"region": "eu1", "count": 1}],
        "cname_records": [],
        "flavor": "wsgi", 
        "install_setup_py": false, 
        "name": "dev", 
        "repo_branch": "master", 
        "repo_commit": "HEAD",
        "requirements_file": "",            
        "wsgiflavor": {
            "wsgi_entrypoint": "wsgiapp.main:application",
            "wsgi_project_root": "wsgiapp"
        }
    }   

Now we deploy the application environment::

    $ thirty deploy wsgiapp dev

    Started deployment (logbook uuid: 8b932504-5e12-11e1-9efc-1a09507dbcf2)
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
    Your application is successfully deployed on http://30loops-app-wsgiapp-dev.30loops.net

.. _`WSGI standard`: http://www.python.org/dev/peps/pep-0333/
.. _`example repository`: https://github.com/crito/wsgiapp↑

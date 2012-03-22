===========================
Deploying WSGI applications
===========================

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

Command line options
--------------------

For common options, please read :doc:`client`.

``--wsgi-entrypoint``
  Set this option to point to the entrypoint created above.


Create a WSGI application
-------------------------

So let's create the application and deploy it. First create the new app and
create an environment:

::

    $ thirty create app wsgiapp git://github.com/30loops/wsgiapp.git --flavor wsgi --root wsgiapp --wsgi-entrypoint wsgiapp.main:application

As you can see, we provided the flavor option, the root directory and the wsgi entrypoint. Now we deploy the application::

    $ thirty deploy wsgiapp production

    Hi! We're now deploying app wsgiapp (environment: production) with the following details:

    name: production
    flavor: wsgi
    requirements_file: requirements.txt
    project_root: wsgiapp
    repo_branch: master
    install_setup_py: False
    repo_commit: HEAD
    database
        name: 30loops-app-wsgiapp-production
        variant: postgresql
        label: database
        username: 30loops-app-wsgiapp-production
        host: 192.168.0.53
        password: NDhkYmQ2YjUz
        port: 9999
    wsgiflavor
        wsgi_entrypoint: main:application
    backends
        count: 1
        region: eu1


    --> Creating a virtualenv for your application, this can take up to 150 seconds......done!
    --> Creating database, this can take up to 10 seconds..done!
    --> Requesting instances, this can take up to 100 seconds....done!
    --> Configuring instances, this can take up to 40 seconds.....done!
    --> Adding the instances to the monitoring systems, this can take up to 10 seconds...done!
    --> Reloading the loadbalancers, this can take up to 30 seconds......done!
    --> Your application is successfully deployed on http://30loops-app-wsgiapp-production.30loops.net

The application is now running on the specified URL.

.. _`WSGI standard`: http://www.python.org/dev/peps/pep-0333/
.. _`example repository`: https://github.com/30loops/wsgiapp↑

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

    $ thirty create app wsgiapp git://github.com/30loops/wsgiapp.git --flavor wsgi --requirements "" --root wsgiapp --wsgi-entrypoint wsgiapp.main:application

As you can see, we provided the flavor option, the root directory and the wsgi entrypoint. Now we deploy the application::

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

The application is now running on the specified URL.

.. _`WSGI standard`: http://www.python.org/dev/peps/pep-0333/
.. _`example repository`: https://github.com/crito/wsgiapp↑

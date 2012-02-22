=================
WSGI Flavor Guide
=================

Using the WSGI flavor, you can host any python web application following the
`WSGI standard`_. This includes a lot of frameworks like flask, web.py and
others.  We offer special support for Django applications.

Lets start creating an example WSGI app. We will create an app as you can see
on our `example repository`_ on github.

The following code is a very basic example for a WSGI app.

.. code-block:: py

    def application(environ, start_response):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers)
        return ['Hello world!\n']

This function serves as an entrypoint for the app server. It is called for each
incoming request. WSGI entrypoints have to be specified in the following
format: ``python.module.path:callable``.

So lets create our application on 30loops and deploy it. First create the new
app and an environment

::

    $ thirty create app wsgiapp

    {
        "environments": [
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
        ],
        "name": "wsgiapp",
        "repository": {
            "location": "git://github.com/crito/wsgiapp.git",
            "name": "wsgiapp",
            "variant": "git"
        },
        "variant": "python"
    }

.. _`WSGI standard`: http://www.python.org/dev/peps/pep-0333/
.. _`example repository`: https://github.com/crito/wsgiapp↑

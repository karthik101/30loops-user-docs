Debugging your application
==========================

When deploying your application on 30loops, you might encounter some errors.
This guide will help you debug your application.

Logbook
-------

The logbook can help you debugging the deployment itself. If you deploy, the 
client will tail the logbook, and show any errors. If errors occur, most likely
there is also a description of the error, which will give you hints on how to
solve them.

If the logbook doesn't give enough information to fix the problem, you should
ask us to help you out.

Logs
----

The logs will help you debugging any errors in your application. This requires
a successful deploy, because logfiles are generated from active instances.

To show logs for an application, you can use the following command::

    thirty logs <app>

This will show the logs of `gunicorn` and `nginx` by default. If you need logs 
of a separate process, you can use the ``--process`` option::

    thirty logs <app> --process nginx

Currently we capture logs from `nginx`, `gunicorn` and `postgres`. To 
limit the number of returned log entries, use the ``--limit`` option.

================
Quickstart guide
================

This guide will take you through the following steps:

1. Installing the 30loops client
2. Creating an application
3. Deploying an application

You need to have a valid account to use the client.

Installing the 30loops client
=============================

Communicating with the 30loops platform can be done using the documented REST api, or using the 30loops client, 
called thirty. The REST api is documented here, in this quickstart we will focus on using the client.
You can install the client using pip. 

    ``pip install thirty-cli``

If pip is not available on your system, you need to install it. On any Debian based system, you can run 

        ``apt-get install python-pip``.

The client is still quite rough, right now it just opens an editor with a preformatted JSON message. You can 
change the variables, and when you save the message, it will be validated and sent to the API. To define the 
editor of your choice, you need to export the EDITOR in your environment. For linux, this can be done by 
running the following command:

   ``export EDITOR=vim``

You can specify the editor of your choice. In Windows it can be done by running:

   ``set EDITOR=c:/winnt/notepad.exe``

Creating an application
=======================

An application on 30loops consists of the following components:

- A repository resource
- An app resource
- An environment

Applications on 30loops are deployed using a pull mechanism. This means, 30loops will connect to your code 
repository, fetch the code, and deploy it on the platform.

Creating an app resource
------------------------

Run the following command (replace myrepo with the desired name of the repository):

    ``thirty create app myapp``

This will open up the previously specified editor, with the following contents:

.. code-block:: js

    {
        "name": "myapp",
        "variant": "python",
        "repository": {
                "location": "",
                "name": "",
                "variant": "git"
                },
        "environments": []
    }

As you can see, the repository details are already included. To create separate repository resources, see the dedicated
chapter.

Enter the name and the location of your repository, for example ``myrepo`` and
``http://github.com/bastichelaar/Django-CMS-30loops.git``, and save the file. It will send the JSON message to 
the api. To verify if the app resource is created correctly, you can run the follewing command:

    ``thirty show app myapp``

It will output something like:

.. code-block:: js

    {
        "name": "myapp", 
        "repository": {
            "href": "http://api.30loops.net/1.0/30loops/repository/myrepo/", 
            "name": "myrepo", 
            "rel": "related"
        }, 
        "variant": "python", 
        "environments": [], 
        "label": "app", 
        "link": {
            "href": "http://api.30loops.net/1.0/30loops/app/myapp/", 
            "rel": "self"
        }
    }

Additionally, the repository resource is also created. To verify, run:

    ``thirty show repository myrepo``
    
It will output something like:

.. code-block:: js

    {
        "link": {
            "href": "http://api.30loops.net/1.0/30loops/repository/myrepo/", 
            "rel": "self"
        }, 
        "location": "http://github.com/bastichelaar/Django-CMS-30loops.git", 
        "variant": "git", 
        "name": "myrepo", 
        "label": "repository"
    }

The app resource is now created. We will continue with creating the application environment.

Creating an environment
-----------------------

For this example, we are using the Django template. You can specify different templates in the future.
Run the following command (replace production with the desired name of the environment):

    ``thirty --template django create app myapp production``

This will open up the previously specified editor, with the following contents:

.. code-block:: js

    {
        "requirements_file": "requirements.txt", 
        "name": "production", 
        "flavor": "django", 
        "djangoflavor": {
            "inject_db": true, 
            "django_project_root": "mycms", 
            "django_settings_module": "settings", 
            "auto_syncdb": false
        }, 
        "repo_branch": "master", 
        "backends": [
            {
                "count": 1, 
                "region": "eu1"
            }
        ], 
        "install_setup_py": false, 
        "repo_commit": "HEAD"
    }

The different variables are explained in the REST api documentation, but are quite self-explaining. the 
``requirements_file`` contains the requirements that will be installed using ``pip``. The ``django_project_root`` is
the directory where your actual Django application (the manage.py) lives. The ``django_settings_module`` is the 
settings module of your application (used for example in ``python manage.py syncdb --settings settings``).

The backends contains the number of backends per zone. At this moment we have two zones:

1. **eu1**, the default zone in Amsterdam
2. **eu2**, the zone in Germany

Note that the database will be automatically created, and will be created in zone **eu1** for now.

If you save this file after filling in the correct variables, it will be validated and sent to the api. To verify if 
your environment is created correctly, run:

    ``thirty show app myapp production``

As you can see, the database resource is automatically created. Your application is now ready for deployment.

Deploying an application
========================

Deploying an application is quite simple and fast, just run the following command:

    ``thirty deploy myapp production``

This will start the deployment on the number of backends you specified. The output of the logbook will be fetched and 
renewed every 10 seconds. You can also access the logbook manually by running:

    ``thirty logbook UUID``

Where UUID is the ID of the deployment task.

After a successfull deploy, your application will be available on the specified DNS name and on 30loops.net, for 
example ``http://30loops-app-myapp-production.30loops.net``.

Additional support
==================

If you have any questions, please log in on ``http://help.30loops.net`` and submit a ticket. You can also chat with us
on #30loops at irc.freenode.net or mail us at support@30loops.net.

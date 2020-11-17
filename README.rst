Album App for Django
====================

ReportBro album application for Django web framework. This is a fully working
demo app to showcase ReportBro and how you can integrate it
in your Django application.

The application is a simple web app and allows to manage a list of music albums.
ReportBro Designer is included so you can modify a template which is used
when you print a pdf of all your albums.

The Demo App is also avaiable for the `Flask <https://palletsprojects.com/p/flask/>`_
and `web2py <http://web2py.com/>`_ web frameworks. See
`Album App for Flask <https://github.com/jobsta/albumapp-flask.git>`_ and
`Album App for web2py <https://github.com/jobsta/albumapp-web2py.git>`_ respectively.

All Instructions in this file are for a Linux/Mac shell but the commands are
easy to adapt for Windows. If a command is different for Windows then
it will be shown below. Commands which can be done in
Windows Explorer (e.g. copy file, create directory) are not explicitly listed
for Windows.

Installation
------------

Clone the git repository and change into the created directory:

.. code:: shell

    $ git clone https://github.com/jobsta/albumapp-django.git
    $ cd albumapp-django

Create a virtual environment called env:

.. code:: shell

    $ python3 -m venv env

Activate the virtual environment:

.. code:: shell

    $ . env/bin/activate

On Windows the virtual environment is activated this way instead:

.. code:: shell

    $ env\Scripts\activate

Once the virtual environment is activated you should see the environment name prepended to the shell prompt.

Install all required dependencies:

.. code:: shell

    $ pip install django reportbro-lib

Configuration
-------------

- Activate the virtual environment (if not already active):

.. code:: shell

    $ . env/bin/activate

- Create a database (albumapp.sqlite) by creating migration scripts and executing them:

.. code:: shell

    $ python manage.py makemigrations albums
    $ python manage.py migrate

- Compile all translation files so the labels can be used in the application (generates django.mo next to django.po):

.. code:: shell

    $ python manage.py compilemessages

Run App
-------

Activate the virtual environment (if not already active):

.. code:: shell

    $ . env/bin/activate

Start the Django webserver:

.. code:: shell

    $ python manage.py runserver

Now your application is running and can be accessed here:
http://127.0.0.1:8000/albums/

IDE Configuration (PyCharm)
---------------------------

1. Open the cloned albumapp-django directory

2. Add virtual env to project:

- Select File -> Settings
- Project: albumapp-django -> Project interpreter
- click Settings-Icon and select "Add Local" option, select the recently created virtual env

Database
--------

sqlite is used as database to store the application data (albums),
report templates and report previews used by ReportBro Designer.

To initially create the db with its tables the following steps are necessary:

Activate the virtual environment (if not already active):

.. code:: shell

    $ . env/bin/activate

Create database migrations:

.. code:: shell

    $ python manage.py makemigrations albums

Execute migration scripts:

.. code:: shell

    $ python manage.py migrate

Translations
------------

Activate virtual environment (if not already active):

.. code:: shell

    $ . env/bin/activate

Run over the entire source tree of the current directory and pull out
all strings marked for translation. It creates (or updates) the django.po message file:

.. code:: shell

    $ python manage.py makemessages

Compile all translation files so labels can be used in the
application (generates django.mo next to django.po):

.. code:: shell

    $ python manage.py compilemessages --ignore env

Python Coding Style
-------------------

The `PEP 8 (Python Enhancement Proposal) <https://www.python.org/dev/peps/pep-0008/>`_
standard is used which is the de-facto code style guide for Python. An easy-to-read version
of PEP 8 can be found at https://pep8.org/

Install on PythonAnywhere
-------------------------

Basically follow the instructions at https://help.pythonanywhere.com/pages/DeployExistingDjangoProject

Upload code to PythonAnywhere:

.. code:: shell

    $ git clone https://github.com/jobsta/albumapp-django.git

In *django_demoapp/settings.py* you have to enter your url in *ALLOWED_HOSTS*, e.g.

.. code:: python

    ALLOWED_HOSTS = ['myuser.pythonanywhere.com']

and set `STATIC_ROOT` accordingly:

.. code:: python

    STATIC_ROOT = '/home/myuser/albumapp-django/albums/static'

On the PythonAnywhere 'Web' Page you have to make sure everything is configured as described
(Source code and working dir, wsgi file, virtualenv). The wsgi file looks something like this:


.. code:: python

    import os
    import sys

    path = '/home/myuser/albumapp-django'
    if path not in sys.path:
        sys.path.append(path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'django_demoapp.settings'
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()

For 'Static files' you enter the following mapping:

URL: /static/

Directory: /home/myuser/albumapp-django/albums/static

Don't forget to perform the necessary installation steps for the django albumapp itself,
i.e. DB migrations and compile translation messages (see above).

Reload the application and run!

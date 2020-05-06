Album App for Django
====================

ReportBro album application for Django web framework. This is a fully working
demo app to showcase ReportBro and how you can integrate it
in your Django application.

The application is a simple web app and allows to manage a list of music albums.
ReportBro Designer is included so you can modify a template which is used
when you print a pdf of all your albums.

All Instructions in this file are for a Linux/Mac shell but the commands should
be easy to adapt for Windows.

Installation
------------

Clone git repository and change into repository dir:

.. code:: shell

    $ git clone https://github.com/jobsta/albumapp-django.git
    $ cd albumapp-django

Create virtual environment:

.. code:: shell

    $ python3 -m venv env

Activate virtual environment:

.. code:: shell

    $ . env/bin/activate

Install dependencies:

.. code:: shell

    $ pip install django reportbro-lib

Configuration
-------------

- Activate virtual environment (if not already active):

.. code:: shell

    $ . env/bin/activate

- Create database (albumapp.sqlite) by creating migration scripts and executing them:

.. code:: shell

    $ python manage.py makemigrations albums
    $ python manage.py migrate

- Compile translation files so labels can be used in the application (generates django.mo next to django.po):

.. code:: shell

    $ python manage.py compilemessages

Run App
-------

Activate virtual environment (if not already active):

.. code:: shell

    $ . env/bin/activate

Start Django webserver:

.. code:: shell

    $ python manage.py runserver

Now your application is running and can be accessed here:
http://127.0.0.1:8000/albums/

IDE Configuration (PyCharm)
---------------------------

1. Open albumapp-django repo directory

2. Add virtual env to project:

- Select File -> Settings
- Project: albumapp-django -> Project interpreter
- click Settings-Icon and select "Add Local" option, select the recently created virtual env

Database
--------

An sqlite database is used to store application data (albums), report templates
and report previews used by ReportBro Designer.

To initially create the db with its tables:

Activate virtual environment (if not already active):

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

Compile translation files so labels can be used in the
application (generates django.mo next to django.po):

.. code:: shell

    $ python manage.py compilemessages --ignore env

Python Coding Style
-------------------

The `PEP 8 (Python Enhancement Proposal) <https://www.python.org/dev/peps/pep-0008/>`_
standard is used which is the de-facto code style guide for Python. An easy-to-read version
of PEP 8 can be found at https://pep8.org/

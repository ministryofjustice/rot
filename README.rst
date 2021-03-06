Register of Technology and Services
===================================

A register containing a list of Technology and Services


Ongoing design considerations
-----------------------------

can be found `here - docs/design_considerations.rst <docs/design_considerations.rst>`_

Requirements
============

Postgres

.. code:: bash

    brew install postgres

Python3

.. code:: bash

    brew install python3

`Virtualenvwrapper <https://virtualenvwrapper.readthedocs.io/en/latest/>`_

Elasticsearch

.. code:: bash

    brew install elasticsearch

GraphViz

.. code:: bash

    brew install graphviz

Setup
=====

To set up the environment:

.. code:: bash

    git clone git@github.com:ministryofjustice/register-of-tech.git
    cd register-of-tech
    cp rot/settings/local.py.example rot/settings/local.py
    mkvirtualenv register-of-tech -p python3
    pip install -r requirements/local.txt

Create the database:

.. code:: bash

    createdb rot
    . bin/reset_db.sh

Load data from Airtable:
You will need to log in to airtable.com and be given access to the database and add your key and app_id to the local.py file

.. code:: python

    AIRTABLE_API_KEY = 'your_api_key'
    AIRTABLE_API_ID = 'airtable_app_id'
    AIRTABLE_WRITE_API_ID = 'airtable_write_app_id'

.. code:: bash

    ./manage.py airtable get

Start Elasticsearch: (in another tab)

.. code:: bash

    elasticsearch

Re-build the cache:

.. code:: bash

    ./manage.py build_index

Start the dev server:

.. code:: bash

    ./manage.py runserver


Visit the API site on http://localhost:8000/api/v1/

Frontend views
==============

View the initial list view on http://localhost:8000/services

Other views are either partial or non-existent at the moment.

Frontend assets
===============

A huge quantity of Sass was ported across from the React app (rot-frontend). It is certain that ~90% of this is not needed, but there has yet to be time to edit and prune it.

All Sass/CSS is compiled into concatenated CSS files by gulp.

To install the necessary gulp files, run

.. code:: bash

    npm install

and then in a new tab run

.. code:: bash

    gulp watch

This will compile and concatenate all Sass/CSS, and also watch the static-src files and recompile on changes.


Build pydot model relationship image
====================================

This will delete all data in the database.

.. code:: bash

    . bin/graph.sh

Testing
=======

Install the packages required for testing

.. code:: bash

    pip install -r requirements/testing.txt

Run the tests

.. code:: bash

    ./manage.py test

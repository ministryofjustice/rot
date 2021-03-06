#!/bin/bash
set -e

# Run migrations if there are any
/usr/bin/python3 manage.py  migrate --settings rot.settings.base --noinput
/usr/bin/python3 manage.py  migrate --run-syncdb --settings rot.settings.base --noinput

# Load fixtures
/usr/bin/python3 manage.py loaddata test_categories test_business_area groups applications

# Set secrets on Person and Application
/usr/bin/python3 manage.py set_secrets

# Run server
/usr/bin/uwsgi --http-socket :$1 --plugin python --ini /app/conf/uwsgi.ini

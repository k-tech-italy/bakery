#!/bin/bash

#### ND: needs pgpass to be setup
#DB_ENGINE=`python manage.py shell --no-imports -c "from django.conf import settings; print(settings.DATABASES['default']['ENGINE'])"`
#DB_HOST=`python manage.py shell --no-imports -c "from django.conf import settings; print(settings.DATABASES['default']['HOST'])"`
#DB_PORT=`python manage.py shell --no-imports -c "from django.conf import settings; print(settings.DATABASES['default']['PORT'], end='')"`
#DB_NAME=`python manage.py shell --no-imports -c "from django.conf import settings; print(settings.DATABASES['default']['NAME'], end='')"`
#
#echo "initializing ${DB_ENGINE} database ${DB_NAME}"
#psql -h ${DB_HOST} -p ${DB_PORT} -U postgres -c "DROP DATABASE IF EXISTS ${DB_NAME}"
#psql -h ${DB_HOST} -p ${DB_PORT} -U postgres -c "CREATE DATABASE ${DB_NAME}"

rm demo.db
./manage.py migrate
if [ "$?" = "0" ]; then
  DJANGO_SUPERUSER_PASSWORD=123 ./manage.py createsuperuser --username admin --email a@a.com --noinput
fi
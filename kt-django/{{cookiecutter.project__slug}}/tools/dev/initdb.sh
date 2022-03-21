#!/bin/bash

### ND: needspgpass to be setup
DB_ENGINE=`python manage.py shell -c "from django.conf import settings; print(settings.DATABASES['default']['ENGINE'])"`
DB_HOST=`python manage.py shell -c "from django.conf import settings; print(settings.DATABASES['default']['HOST'])"`
DB_PORT=`python manage.py shell -c "from django.conf import settings; print(settings.DATABASES['default']['PORT'], end='')"`
DB_NAME=`python manage.py shell -c "from django.conf import settings; print(settings.DATABASES['default']['NAME'], end='')"`

echo initializing ${DB_ENGINE} database ${DB_NAME}
psql -h ${DB_HOST} -p ${DB_PORT} -U postgres -c "DROP DATABASE IF EXISTS test_${DB_NAME}"
psql -h ${DB_HOST} -p ${DB_PORT} -U postgres -c "DROP DATABASE IF EXISTS ${DB_NAME}"
psql -h ${DB_HOST} -p ${DB_PORT} -U postgres -c "CREATE DATABASE ${DB_NAME}"
psql -h ${DB_HOST} -p ${DB_PORT} -U postgres -d "${DB_NAME}" -c "CREATE SCHEMA django" ; \
for schema in `python manage.py shell -c "from django.conf import settings; print('\t'.join(settings.DATABASE_APPS))"`; do \
		psql -h ${DB_HOST} -p ${DB_PORT} -U postgres -d "${DB_NAME}" -c "DROP SCHEMA IF EXISTS $schema CASCADE" ; \
		psql -h ${DB_HOST} -p ${DB_PORT} -U postgres -d "${DB_NAME}" -c "CREATE SCHEMA $schema" ; \
	 done
#!/bin/sh
set -e

ROLE="${1:-web}"
shift || true

case "$ROLE" in
  web)
    echo "Running upgrade..."
    django-admin upgrade

    echo "Exporting URL prefixes..."
    django-admin export_url_prefixes --output /shared/url_prefixes.json

    echo "Starting uWSGI..."
    exec uwsgi --ini /app/uwsgi.ini "$@"
    ;;
  {% if cookiecutter.use_celery == "yes" %}worker)
    echo "Starting Celery worker..."
    exec celery -A {{ cookiecutter.package_name }}.config worker --loglevel=info "$@"
    ;;
  {% endif %}*)
    echo "Unknown role: $ROLE. Valid roles: web{% if cookiecutter.use_celery == "yes" %} | worker{% endif %}" >&2
    exit 1
    ;;
esac
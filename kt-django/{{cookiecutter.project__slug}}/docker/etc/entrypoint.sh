#!/bin/bash -e

STATIC_ROOT={{cookiecutter.environ__prefix}}_STATIC_ROOT
MEDIA_ROOT={{cookiecutter.environ__prefix}}_MEDIA_ROOT
ADMIN_USERNAME={{cookiecutter.environ__prefix}}_ADMIN_USERNAME
ADMIN_EMAIL={{cookiecutter.environ__prefix}}_ADMIN_EMAIL
ADMIN_PASSWORD={{cookiecutter.environ__prefix}}_ADMIN_PASSWORD
CELERY_BROKER_URL={{cookiecutter.environ__prefix}}_CELERY_BROKER_URL

mkdir -p "/{{cookiecutter.project__slug}}/logs" "${STATIC_ROOT}" "${MEDIA_ROOT}"
chown {{cookiecutter.project__slug}} -R /{{cookiecutter.project__slug}} "${STATIC_ROOT}" "${MEDIA_ROOT}"

echo "$*"

setup() {
  gosu {{cookiecutter.project__slug}} django-admin upgrade -vv \
          --admin-username ${ADMIN_USERNAME:-admin} \
          --admin-email ${ADMIN_EMAIL} \
          --admin-password ${ADMIN_PASSWORD}
}
if [ "${STACK_PROTOCOL}" = "https" ]; then
      echo "setting up HTTPS"
      STACK_PORT="8443,/etc/certs/cbtcsudan.crt,/etc/certs/cbtcsudan.key"
else
      echo "setting up HTTP"
      STACK_PORT=8000
fi

if [ "$*" = "run" ]; then
  setup
  exec gosu {{cookiecutter.project__slug}} uwsgi --${STACK_PROTOCOL} 0.0.0.0:${STACK_PORT} \
    --static-map "/static=${{cookiecutter.environ__prefix}}_STATIC_ROOT" \
    --static-map "/media=${{cookiecutter.environ__prefix}}_MEDIA_ROOT" \
    --master \
    --module {{cookiecutter.project__slug}}.config.wsgi \
    --processes 4 \
    --offload-threads 8
elif [ "$*" = "worker" ]; then
  setup
  celery -A {{cookiecutter.project__slug}}.config.celery worker --loglevel=INFO  -n wk_%h
elif [ "$*" = "stack" ]; then
  setup
  export STACK_PROTOCOL
  export STACK_PORT
  exec gosu {{cookiecutter.project__slug}} circusd /etc/circus.conf
elif [ "$*" = "dev" ]; then
  setup
  exec gosu {{cookiecutter.project__slug}} django-admin runserver 0.0.0.0:8000
elif [ "$*" = "flower" ]; then
  exec gosu {{cookiecutter.project__slug}} -A {{cookiecutter.project__slug}}.config.celery --broker=${CELERY_BROKER_URL} flower
elif [ "$*" = "beat" ]; then
  setup
  celery -A {{cookiecutter.project__slug}}.config.celery beat --loglevel=INFO
else
  exec "$@"
fi

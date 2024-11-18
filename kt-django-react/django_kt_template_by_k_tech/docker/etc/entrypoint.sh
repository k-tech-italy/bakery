#!/bin/bash -e

STATIC_ROOT=DJANGOKTTEMPLATEBYKTECH_STATIC_ROOT
MEDIA_ROOT=DJANGOKTTEMPLATEBYKTECH_MEDIA_ROOT
ADMIN_USERNAME=DJANGOKTTEMPLATEBYKTECH_ADMIN_USERNAME
ADMIN_EMAIL=DJANGOKTTEMPLATEBYKTECH_ADMIN_EMAIL
ADMIN_PASSWORD=DJANGOKTTEMPLATEBYKTECH_ADMIN_PASSWORD
CELERY_BROKER_URL=DJANGOKTTEMPLATEBYKTECH_CELERY_BROKER_URL

mkdir -p "/django_kt_template_by_k_tech/logs" "${STATIC_ROOT}" "${MEDIA_ROOT}"
chown django_kt_template_by_k_tech -R /django_kt_template_by_k_tech "${STATIC_ROOT}" "${MEDIA_ROOT}"

echo "$*"

setup() {
  gosu django_kt_template_by_k_tech django-admin upgrade -vv \
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
  exec gosu django_kt_template_by_k_tech uwsgi --${STACK_PROTOCOL} 0.0.0.0:${STACK_PORT} \
    --static-map "/static=$DJANGOKTTEMPLATEBYKTECH_STATIC_ROOT" \
    --static-map "/media=$DJANGOKTTEMPLATEBYKTECH_MEDIA_ROOT" \
    --master \
    --module django_kt_template_by_k_tech.config.wsgi \
    --processes 4 \
    --offload-threads 8
elif [ "$*" = "worker" ]; then
  setup
  celery -A django_kt_template_by_k_tech.config.celery worker --loglevel=INFO  -n wk_%h
elif [ "$*" = "stack" ]; then
  setup
  export STACK_PROTOCOL
  export STACK_PORT
  exec gosu django_kt_template_by_k_tech circusd /etc/circus.conf
elif [ "$*" = "dev" ]; then
  setup
  exec gosu django_kt_template_by_k_tech django-admin runserver 0.0.0.0:8000
elif [ "$*" = "flower" ]; then
  exec gosu django_kt_template_by_k_tech -A django_kt_template_by_k_tech.config.celery --broker=${CELERY_BROKER_URL} flower
elif [ "$*" = "beat" ]; then
  setup
  celery -A django_kt_template_by_k_tech.config.celery beat --loglevel=INFO
else
  exec "$@"
fi

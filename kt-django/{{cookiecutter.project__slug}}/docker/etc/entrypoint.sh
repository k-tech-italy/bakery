#!/bin/bash -e

echo "$*"

mkdir -p "/{{cookiecutter.project__slug}}/logs" "${{cookiecutter.environ__prefix}}STATIC_ROOT}" "${{cookiecutter.environ__prefix}}MEDIA_ROOT}"
chown {{cookiecutter.project__slug}} -R /{{cookiecutter.project__slug}} "${{cookiecutter.environ__prefix}}STATIC_ROOT}" "${{cookiecutter.environ__prefix}}MEDIA_ROOT}"

echo "$*"

setup() {
  gosu {{cookiecutter.project__slug}} django-admin upgrade -vv \
          --migrate all --verbosity 1 \
          --admin-username ${{cookiecutter.environ__prefix}}ADMIN_USERNAME:-admin} \
          --admin-email ${{cookiecutter.environ__prefix}}ADMIN_EMAIL} \
          --admin-password ${{cookiecutter.environ__prefix}}ADMIN_PASSWORD}
}
if [ "${STACK_PROTOCOL}" = "https" ]; then
      echo "setting up HTTPS"
      STACK_PORT="8443,/etc/certs/{{cookiecutter.project__slug}}.crt,/etc/certs/{{cookiecutter.project__slug}}.key"
else
      echo "setting up HTTP"
      STACK_PORT=8000
fi

if [ "$*" = "run" ]; then
  setup
  exec gosu {{cookiecutter.project__slug}} uwsgi --${STACK_PROTOCOL} 0.0.0.0:${STACK_PORT} \
    --static-map "/static=${{cookiecutter.environ__prefix}}STATIC_ROOT" \
    --static-map "/media=${{cookiecutter.environ__prefix}}MEDIA_ROOT" \
    --master \
    --module {{cookiecutter.project__slug}}.config.wsgi \
    --processes 4 \
    --offload-threads 8
elif [ "$*" = "upgrade" ]; then
  setup
elif [ "$*" = "upgrade-schemas" ]; then
  gosu {{cookiecutter.project__slug}} django-admin upgrade \
          --migrate ${{cookiecutter.environ__prefix}}DATABASE_APPS} --verbosity 1
elif [ "$*" = "stack" ]; then
  setup
  export STACK_PROTOCOL
  export STACK_PORT
  exec gosu {{cookiecutter.project__slug}} circusd /etc/circus.conf
elif [ "$*" = "dev" ]; then
  setup
  exec gosu {{cookiecutter.project__slug}} django-admin runserver 0.0.0.0:8000
else
  exec "$@"
fi

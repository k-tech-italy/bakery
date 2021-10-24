ARG BASE_IMAGE
ARG DOCKER_REGISTRY
FROM ${DOCKER_REGISTRY}/kt/{{cookiecutter.project__slug}}/base:${BASE_IMAGE}

ENV DJANGO_SETTINGS_MODULE="{{cookiecutter.project__slug}}.config.settings" \
	{{cookiecutter.environ__prefix}}MEDIA_ROOT="/tmp/media" \
    {{cookiecutter.environ__prefix}}ADMIN_EMAIL="" \
    {{cookiecutter.environ__prefix}}ADMIN_PASSWORD="" \
    {{cookiecutter.environ__prefix}}ADMIN_USERNAME="" \
    {{cookiecutter.environ__prefix}}CELERY_BROKER="" \
    {{cookiecutter.environ__prefix}}DATABASE_URL="" \
    {{cookiecutter.environ__prefix}}MINIO_CONF_VALIDATION="" \
    {{cookiecutter.environ__prefix}}MINIO_ENDPOINT_URL="" \
    {{cookiecutter.environ__prefix}}MINIO_PORT="" \
    {{cookiecutter.environ__prefix}}MINIO_SECURE="" \
    {{cookiecutter.environ__prefix}}REDIS_CACHE_URL="" \
    {{cookiecutter.environ__prefix}}SECRET_KEY="" \
    {{cookiecutter.environ__prefix}}STATIC_ROOT="/tmp/static"

EXPOSE 8000
EXPOSE 8443
ADD . /code
WORKDIR /code
VOLUME /etc/certs

RUN sha1sum -c /CHECKSUM
RUN pip install . --no-deps -vv \
    && rm -fr /code

COPY docker/etc/entrypoint.sh /usr/local/bin/docker-entrypoint.sh
COPY docker/etc/circus.conf /etc/circus.conf


ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["stack"]

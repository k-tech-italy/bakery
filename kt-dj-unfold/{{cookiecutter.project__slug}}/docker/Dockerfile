ARG BASE_IMAGE
ARG DOCKER_REGISTRY

FROM ${DOCKER_REGISTRY}/kt/{{cookiecutter.project_slug}}/base:${BASE_IMAGE}

ENV DJANGO_SETTINGS_MODULE="{{cookiecutter.project_module}}.config.settings"
ENV	MEDIA_ROOT="/data/media"
ENV	STATIC_ROOT="/data/static"

WORKDIR /code

#RUN sha1sum -c /CHECKSUM

ADD . /code

RUN chown -R ktech:ktech /code/*

USER ktech

SHELL ["/bin/bash", "-c"]

#ADD tools/zapdata/demo tools/zapdata/demo
RUN pip install . --no-deps -vv && rm -fr src dist docker
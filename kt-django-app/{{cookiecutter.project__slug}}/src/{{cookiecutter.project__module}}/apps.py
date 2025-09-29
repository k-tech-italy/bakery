"""{{ cookiecutter.project__name }} app config."""

from django.apps import AppConfig


class Config(AppConfig):  # noqa: D101
    verbose_name = "{{ cookiecutter.project__name }}"
    name = "{{ cookiecutter.project__module }}"

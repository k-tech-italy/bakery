"""{{ cookiecutter.project__name }} app config."""

from django.apps import AppConfig
from typing_extensions import override


class Config(AppConfig):  # noqa: D101
    verbose_name = "{{ cookiecutter.project__name }}"
    name = "{{ cookiecutter.project__module }}"

    @override
    def ready(self) -> None:
        from . import checks  # noqa
        from . import signals  # noqa

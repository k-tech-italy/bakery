from django.apps import AppConfig


class Config(AppConfig):
    verbose_name = "{{ cookiecutter.project__name }}"
    name = "{{ cookiecutter.project__module }}"

    def ready(self) -> None:
        from . import checks  # noqa

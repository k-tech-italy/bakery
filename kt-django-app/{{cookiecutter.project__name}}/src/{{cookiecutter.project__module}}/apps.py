from django.apps import AppConfig


class Config(AppConfig):
    verbose_name = "Smart Env"
    name = "{{ cookiecutter.project__module }}"

    def ready(self) -> None:
        from . import checks  # noqa

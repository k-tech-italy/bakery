from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "{{ cookiecutter.project__module }}.core"
    default_auto_field = "django.db.models.AutoField"

    def ready(self):
        from {{ cookiecutter.project__module }}.core import admin  # noqa: F401

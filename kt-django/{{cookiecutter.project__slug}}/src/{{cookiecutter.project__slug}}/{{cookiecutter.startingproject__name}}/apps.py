from django.apps import AppConfig


class {{cookiecutter.startingproject__name|replace('_', ' ')|title|replace(' ', '')}}Config(AppConfig):
    name = '{{cookiecutter.project__slug}}.{{cookiecutter.startingproject__name}}'
    default_auto_field = 'django.db.models.AutoField'

    def ready(self):
        from {{cookiecutter.project__slug}}.{{cookiecutter.startingproject__name}} import admin  # noqa: F401

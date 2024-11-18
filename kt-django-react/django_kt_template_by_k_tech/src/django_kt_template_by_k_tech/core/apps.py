from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'django_kt_template_by_k_tech.core'
    default_auto_field = 'django.db.models.AutoField'

    def ready(self):
        from django_kt_template_by_k_tech.core import admin  # noqa: F401

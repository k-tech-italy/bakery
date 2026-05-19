import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{ cookiecutter.package_name }}.config.settings")

app = Celery("{{ cookiecutter.package_name }}")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

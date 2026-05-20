__version__ = "0.1.0"
{% if cookiecutter.use_celery == "yes" %}
from .config.celery import app as celery_app

__all__ = ("celery_app",)
{% endif -%}

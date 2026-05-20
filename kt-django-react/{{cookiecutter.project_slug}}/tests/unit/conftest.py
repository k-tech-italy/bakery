import os

import pytest


def pytest_configure(config: pytest.Config) -> None:
    os.environ["DEBUG"] = "False"
    os.environ["LOGGING_LEVEL"] = "ERROR"{% if cookiecutter.use_sentry == "yes" %}
    os.environ["SENTRY_DSN"] = ""{% endif %}

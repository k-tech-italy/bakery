from django.utils.translation import gettext_lazy as _

from {{cookiecutter.project__module}} import __author__
from {{cookiecutter.project__module}}.config import env
from {{cookiecutter.project__module}}.version import __version__

UNFOLD_APPS = [
    "unfold",  # before django.contrib.admin
    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.forms",  # optional, if special form elements are needed
    "unfold.contrib.inlines",  # optional, if special inlines are needed
    "unfold.contrib.import_export",  # optional, if django-import-export package is used
    "unfold.contrib.guardian",  # optional, if django-guardian package is used
    "unfold.contrib.simple_history",  # optional, if django-simple-history package is used
    "unfold.contrib.location_field",  # optional, if django-location-field package is used
    "unfold.contrib.constance",  # optional, if django-constance package is used
]


def get_environment(request):
    """
    Callback has to return a list of two values represeting text value and the color
    type of the label displayed in top right corner.
    """
    environ = env("ENVIRONMENT").upper()
    if environ == "LOCAL":
        return [environ, "success"]
    elif environ.startswith("PROD"):
        return ["PROD", "danger"]
    elif environ.startswith("QA") or environ.startswith("INT"):
        return [environ, "warning"]

    return [environ, "info"]  # info, danger, warning, success


UNFOLD = {
    "SITE_TITLE": "{{cookiecutter.project__name}}",
    "SITE_HEADER": "{{cookiecutter.project__name}} " + __version__,
    "ENVIRONMENT": get_environment,
    "SITE_DROPDOWN": [
        {
            "icon": "diamond",
            "title": "K-Tech",
            "link": "https://www.k-tech.it",
            "attrs": {
                "target": "_blank",
            },
        },
        {
            "icon": "docs",
            "title": "Documentation",
            "link": "https://k-tech-italy.github.io/{{cookiecutter.project__module}}/",
            "attrs": {
                "target": "_blank",
            },
        },
    ],
    "COMMAND": {  # https://unfoldadmin.com/docs/configuration/command/
        "search_models": True,
        # "search_callback": "utils.search_callback",
        "show_history": True,
    },
}

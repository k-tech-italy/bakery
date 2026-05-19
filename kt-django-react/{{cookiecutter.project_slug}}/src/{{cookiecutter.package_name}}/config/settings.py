import environ
{% if cookiecutter.use_sentry == "yes" %}import sentry_sdk
{% endif %}
from pathlib import Path

import {{ cookiecutter.package_name }}

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    ENVIRONMENT=(str, "LOCAL"),
    SECRET_KEY=(str, "local"),
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
    LOCAL_APPS=(list, []),
    DATABASE_URL=(str, "sqlite:///{{ cookiecutter.package_name }}.db"),
    STATIC_ROOT=(str, "~data/static"),
    STATIC_URL=(str, "/static/"),
    MEDIA_ROOT=(str, "~data/media"),
    MEDIA_URL=(str, "/media/"),
    TIME_ZONE=(str, "UTC"),
    LOGGING_LEVEL=(str, "ERROR"),
    CORS_ALLOWED_ORIGINS=(list, ["http://localhost:5173"]),
    CSRF_TRUSTED_ORIGINS=(list, []),{% if cookiecutter.use_sentry == "yes" %}
    SENTRY_DSN=(str, ""),{% endif %}{% if cookiecutter.use_celery == "yes" %}
    CELERY_BROKER_URL=(str, "redis://localhost:6379/0"),{% endif %}
)

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

{% if cookiecutter.use_sentry == "yes" %}if SENTRY_DSN := env("SENTRY_DSN"):
    from sentry_sdk.integrations.django import DjangoIntegration{% if cookiecutter.use_celery == "yes" %}
    from sentry_sdk.integrations.celery import CeleryIntegration{% endif %}

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        release={{ cookiecutter.package_name }}.__version__,
        debug=env("DEBUG"),
        environment=env("ENVIRONMENT"),
        send_default_pii=True,
        default_integrations=False,
        integrations=[
            DjangoIntegration(),{% if cookiecutter.use_celery == "yes" %}
            CeleryIntegration(),{% endif %}
        ],
    )

{% endif %}DEFAULT_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRDPARTY_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
    "drf_spectacular",
    "corsheaders",
    "django_filters",
]

USER_APPS = [
    "{{ cookiecutter.package_name }}",
    "{{ cookiecutter.package_name }}.{{ cookiecutter.first_app_name }}",
]

LOCAL_APPS = env.list("LOCAL_APPS")

INSTALLED_APPS = [*DEFAULT_APPS, *THIRDPARTY_APPS, *USER_APPS, *LOCAL_APPS]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "{{ cookiecutter.package_name }}.config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "{{ cookiecutter.package_name }}.config.wsgi.application"

DATABASES = {"default": env.db_url("DATABASE_URL")}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = env("TIME_ZONE")
USE_I18N = True
USE_TZ = True

STATIC_ROOT = env("STATIC_ROOT")
STATIC_URL = env("STATIC_URL")
MEDIA_ROOT = env("MEDIA_ROOT")
MEDIA_URL = env("MEDIA_URL")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.DjangoModelPermissions"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "{{ cookiecutter.project_name }} API",
    "DESCRIPTION": "{{ cookiecutter.description }}",
    "VERSION": {{ cookiecutter.package_name }}.__version__,
    "COMPONENT_SPLIT_REQUEST": True,
    "SERVE_INCLUDE_SCHEMA": False,
    "POSTPROCESSING_HOOKS": [
        "drf_spectacular.hooks.postprocess_schema_enums",
        "{{ cookiecutter.package_name }}.{{ cookiecutter.first_app_name }}.api.openapi.add_tags",
    ],
}

CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")

{% if cookiecutter.use_celery == "yes" %}CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_TASK_TRACK_STARTED = True

{% endif %}LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s - %(asctime)s - %(name)s %(funcName)s:%(lineno)d :: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "short": {
            "format": "%(levelname)s - %(name)s %(funcName)s:%(lineno)d :: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "ERROR",
            "class": "logging.StreamHandler",
            "formatter": "short",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "django": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        "{{ cookiecutter.package_name }}": {
            "level": env("LOGGING_LEVEL"),
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

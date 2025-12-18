from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    type ItemValue = str | bool | int | list[str] | None
    type ConfigItem = tuple[type, ItemValue] | tuple[type, ItemValue, str] | tuple[type, ItemValue, str, Any]

from smart_env import SmartEnv

CONFIG = {
    "ALLOWED_HOSTS": (list, [], ["127.0.0.1", "localhost"], False, "The hosts allowed"),
    "DEBUG": (bool, False, True, False, "https://docs.djangoproject.com/en/5.1/ref/settings/#debug"),
    "DATABASE_URL": (
        str,
        "",
        "sqlite://demo.db",
        False,
        "https://docs.djangoproject.com/en/5.1/ref/settings/#DATABASES",
    ),
    "EMAIL_BACKEND": (
        str,
        "django.core.mail.backends.console.EmailBackend",
        "django.core.mail.backends.console.EmailBackend",
        False,
        "https://docs.djangoproject.com/en/5.1/ref/settings/#email-backend",
    ),
    "USE_TZ": (bool, True, True, False, "https://docs.djangoproject.com/en/5.1/ref/settings/#debug"),
    "SECURE_SSL_REDIRECT": (
        bool,
        True,
        False,
        False,
        "https://docs.djangoproject.com/en/5.1/ref/settings/#SECURE_SSL_REDIRECT",
    ),
    "SESSION_COOKIE_SECURE": (
        bool,
        True,
        False,
        False,
        "https://docs.djangoproject.com/en/5.1/ref/settings/#SESSION_COOKIE_SECURE",
    ),
    "SECRET_KEY": (str, "", "<insecure_key>", False, "Django SECRET_KEY"),
}

env = SmartEnv(**CONFIG)

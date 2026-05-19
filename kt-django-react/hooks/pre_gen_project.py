import re
import sys

SLUG_RE = re.compile(r"^[a-z][a-z0-9-]+$")
PKG_RE = re.compile(r"^[a-z][a-z0-9_]+$")
APP_RE = re.compile(r"^[a-z][a-z0-9_]+$")

errors = []

if not SLUG_RE.match("{{ cookiecutter.project_slug }}"):
    errors.append(
        "project_slug '{{ cookiecutter.project_slug }}' is invalid. "
        "Use lowercase letters, digits, and hyphens only (must start with a letter)."
    )

if not PKG_RE.match("{{ cookiecutter.package_name }}"):
    errors.append(
        "package_name '{{ cookiecutter.package_name }}' is invalid. "
        "Use lowercase letters, digits, and underscores only (must start with a letter)."
    )

if not APP_RE.match("{{ cookiecutter.first_app_name }}"):
    errors.append(
        "first_app_name '{{ cookiecutter.first_app_name }}' is invalid. "
        "Use lowercase letters, digits, and underscores only (must start with a letter)."
    )

if errors:
    for msg in errors:
        print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)
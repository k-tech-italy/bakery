# Project Structure

## Overview

{{ cookiecutter.project__name }} is a Django project scaffolding that provides a production-ready foundation with modern development tools and best practices.

## Directory Layout

```
{{ cookiecutter.project__slug }}/
├── .agents/              # AI agent context files (this directory)
├── dist/                 # Built packages
├── docs/                 # Documentation (MKDocs)
├── docker/               # Docker container definitions
│   ├── certs/            # SSL certificates
│   └── etc/              # Configuration files for containers
├── src/
│   └── {{ cookiecutter.project__slug }}/          # Main application package
│       ├── __init__.py
│       ├── version.py    # Auto-generated version file (DO NOT EDIT)
│       ├── config/       # Django configuration fragments
│       │   ├── defaults.py
│       │   ├── settings.py      # Main Django settings
│       │   ├── urls.py          # URL routing
│       │   ├── wsgi.py          # WSGI entry point
│       │   ├── asgi.py          # ASGI entry point
│       │   └── fragments/       # Modular config pieces
│       │       ├── constance.py     # Dynamic configuration
│       │       ├── crispy.py        # Form rendering
│       │       ├── ddt.py           # Debug toolbar
│       │       ├── flags.py         # Feature flags
│       │       ├── security.py      # Security settings
│       │       ├── sentry.py        # Error tracking
│       │       └── unfold.py        # Admin interface
│       ├── core/         # Core app with admin models
│       ├── management/   # Custom Django management commands
│       ├── cli/          # CLI utilities
│       ├── web/          # Web templates and views
│       ├── exceptions.py
│       ├── flags.py      # Feature flag helpers
│       └── sentry.py     # Sentry integration
├── tests/                # Test suite
├── devops/               # DevOps scripts and configurations
├── tools/                # Development tools and helpers
├── .agents.md            # This project's documentation
├── CONTRIBUTING.md       # Contribution guidelines
├── Makefile              # Common development tasks
├── manage.py             # Django CLI entry point
├── pyproject.toml        # Project dependencies (UV)
├── ruff.toml             # Ruff linter configuration
├── pytest.ini            # Pytest test runner configuration
└── system.py             # System-wide state and locking
```

## Key Components

### Core Application (`src/{{ cookiecutter.project__slug }}`)

The main application package containing:

- **Configuration**: Modular Django settings using fragment patterns
- **Core App**: Base models, admin interface, and common utilities
- **Web Layer**: Public-facing templates and views (home, trees, tables)
- **CLI Tools**: Custom management commands for upgrades and maintenance

### Configuration Pattern

Settings are organized using a **fragment pattern** in `src/{{ cookiecutter.project__slug }}/config/fragments/`:

```
constance.py   # Dynamic runtime configuration
crispy.py      # Django-crispy-forms settings
ddt.py         # Debug toolbar configuration
flags.py       # Feature flags (django-flags)
security.py    # Security middleware and settings
sentry.py      # Sentry error tracking integration
unfold.py      # Django-Unfold admin interface
```

Fragments are imported into `settings.py` using wildcard imports:

```python
from .fragments.constance import *  # noqa: F401,F403
from .fragments.unfold import *     # noqa: F401,F403
# ...
```

### Admin Interface (Django-Unfold)

The project uses [Django-Unfold](https://unfoldadmin.com) as the admin interface, configured in `settings.py`:

- Customized with environment badges (LOCAL/PROD/QA)
- K-Tech branding and documentation links
- Enhanced search, history, and command features

### Feature Flags

Uses [django-flags](https://github.com/caktus/django-flags) for feature toggles:
- Configured in `src/{{ cookiecutter.project__slug }}/config/fragments/flags.py`
- Runtime evaluation via `flag_enabled()`

## Development Environment

### Prerequisites

- **UV**: Package manager, venv manager, and Python binary installer
- **Ruff**: Code linter and formatter
- **Pre-commit**: Git hooks for code quality
- **Direnv** (optional): Automatic environment configuration

### Environment Variables

See `.env.example` for the complete list. Key variables:

```bash
DJANGO_SETTINGS_MODULE={{ cookiecutter.project__slug }}.config.settings
SECRET_KEY=<your-secret-key>
DEBUG=True/False
DATABASE_URL=postgres://user:pass@host/db
ADMIN_EMAIL=admin@example.com
ADMIN_USERNAME=admin
ADMIN_PASSWORD=<admin-password>
SENTRY_DSN=<sentry-dsn>  # Optional error tracking
ENVIRONMENT=local|development|qa|production
```

## Deployment

### Docker Container

See `docker/Dockerfile` and `docker/etc/entrypoint.sh`:

- Base image: `${DOCKER_REGISTRY}/kt/{{ cookiecutter.project__slug }}/base:${BASE_IMAGE}`
- User: `ktech`
- Static/media paths: `/data/static`, `/data/media`
- Entry points: run, worker, dev, flower, beat

### Management Commands

```bash
# Setup/Upgrade database and static files
./manage.py upgrade [--migrate] [--static]

# Demo data setup
./manage.py demo

# Run server (development)
./manage.py runserver
```

### Makefile Targets

The project uses two Makefiles for common tasks:

#### Root Makefile (`Makefile`)

| Target | Description |
|--------|-------------|
| `make help` | Show all available targets with descriptions |
| `make develop` | Initialize project (git, venv, env files) |
| `make static` | Build static assets (Sass/webpack + collectstatic) |
| `make lint` | Run pre-commit hooks on all files |
| `make test` | Run pytest test suite |
| `make bump` | Increment version (major/minor/patch) |
| `make clean` | Remove build artifacts and caches |
| `make fullclean` | Full cleanup (removes .venv, node_modules) |
| `make build` | Build Tailwind CSS + sdist package |
| `make detect-secrets` | Scan for secrets in codebase |

#### Docker Makefile (`docker/Makefile`)

Requires: `DOCKER_REGISTRY`, `DOCKER_USR`, `DOCKER_PWD`

| Target | Description |
|--------|-------------|
| `make help` | Show available docker targets |
| `make build-base` | Build base image with dependencies |
| `make build` | Build application image |
| `make registrylogin` | Log in to Docker registry (ECR or custom) |
| `make release` | Push image to registry |
| `make release-latest` | Tag and push as latest version |
| `make run` | Run container locally with HTTP (port 8000) |
| `make runs` | Run container locally with HTTPS (port 443) |

For detailed Makefile usage, see the [Tooling Guide](tooling.md).

## Testing

- **Framework**: pytest
- **Coverage**: configured in `tests/.coveragerc`
- **Run**: `pytest tests/` or `tox`

## Linting & Formatting

- **Tool**: Ruff (fast Python linter/formatter)
- **Config**: `ruff.toml`
- **Pre-commit hooks**: defined in `.pre-commit-config.yaml`
- **Run**: `ruff check . --fix` and `ruff format`

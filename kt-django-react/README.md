# cookiecutter-django-react

A production-ready project template for Django + React applications.

## Stack

- **Backend**: Python · Django · DRF · uv
- **Frontend**: React 19 · TypeScript · Vite 7 · Tailwind v4
- **Database**: PostgreSQL (+ optional Redis / Celery)
- **Deployment**: Docker Compose · uWSGI · nginx
- **Tooling**: ruff · mypy · pre-commit · detect-secrets · commitizen · pytest · vitest

## Prerequisites

- [cookiecutter](https://cookiecutter.readthedocs.io/) (`pip install cookiecutter` or `uv tool install cookiecutter`)
- [cookiecutter-extensions](https://github.com/cjolowicz/cookiecutter-extensions) (`pip install cookiecutter-extensions`) — required for `{% now %}` in LICENSE

## Variables

| Variable | Default | Description |
|---|---|---|
| `project_name` | `My Project` | Human-readable project name |
| `project_slug` | `my-project` | Repo / Docker image name (lowercase, hyphens) |
| `package_name` | `myproject` | Python package name (lowercase, underscores) |
| `first_app_name` | `core` | Name of the first Django app |
| `description` | — | One-line project description |
| `author_name` | — | Author full name |
| `author_email` | — | Author email address |
| `python_version` | `3.13` | Python version for `.python-version` and Dockerfile |
| `django_version` | `5.2` | Django version pinned in `pyproject.toml` |
| `postgres_version` | `17` | PostgreSQL image tag in `docker-compose.yml` |
| `redis_version` | `8` | Redis image tag (only used when `use_celery == "yes"`) |
| `use_celery` | `yes` | Include Celery + Redis worker service |
| `use_sentry` | `yes` | Include Sentry SDK and `SENTRY_DSN` env var |
| `use_mkdocs` | `yes` | Include MkDocs docs site and `docs.yml` CI workflow |
| `use_trivy` | `yes` | Include Trivy container scanning and `docker.yml` CI workflow |
| `open_source_license` | `MIT` | `MIT`, `Apache-2.0`, or `none` |

## After generation

```bash
cd <project_slug>
uv sync
cd frontend && npm install && cd ..
uv run pre-commit install --install-hooks
cp .env.example .env        # fill in DATABASE_URL etc.
uv run detect-secrets scan > .secrets.baseline
uv run manage.py upgrade
```

See the generated `CONTRIBUTING.md` for the full developer setup guide.

## What you get

```
<project_slug>/
├── src/<package_name>/        # Django project (config/, management/, <first_app>/)
├── tests/                     # pytest (unit/, functional/, integration/, fixtures)
├── frontend/                  # React + Vite + Vitest
├── docker/                    # Multi-stage Dockerfiles for app + nginx
├── .github/workflows/         # check.yml · test.yml · docker.yml · docs.yml
├── docs/                      # MkDocs (if use_mkdocs == "yes")
├── AGENTS.md                  # AI-agent coding conventions
└── CONTRIBUTING.md            # Developer setup guide
```

## Template development

See [AGENTS.md](AGENTS.md) for variable map, Jinja2 rules, and instructions for adding
feature toggles.
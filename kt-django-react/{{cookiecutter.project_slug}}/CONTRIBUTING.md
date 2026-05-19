# Contributing

## Prerequisites

- [uv](https://docs.astral.sh/uv)
- [direnv](https://direnv.net/)
- [nvm](https://github.com/nvm-sh/nvm)
- Node {{ cookiecutter.python_version }} (via `.nvmrc`)
- Python {{ cookiecutter.python_version }} (via `.python-version`)
- PostgreSQL {{ cookiecutter.postgres_version }}{% if cookiecutter.use_celery == "yes" %} + Redis {{ cookiecutter.redis_version }}{% endif %}

## First-time setup

```bash
# 1. Copy and activate environment files
cp .env.example .env        # fill in DATABASE_URL and other vars
cp .envrc.example .envrc
direnv allow                # installs deps and activates venv automatically

# 2. Install frontend dependencies
cd frontend && npm install && cd ..

# 3. Install pre-commit hooks
uv run pre-commit install --install-hooks

# 4. Create the detect-secrets baseline
uv run detect-secrets scan > .secrets.baseline

# 5. Apply database migrations and create the admin user
uv run manage.py upgrade
```

## Running the app locally

```bash
# Backend (port 8000)
uv run manage.py runserver

# Frontend dev server (port 5173, proxies /api to localhost:8000)
cd frontend && npm run dev
```

## Running tests

```bash
# All tests
uv run pytest tests/

# Skip slow functional (browser) tests
uv run pytest tests/ --no-functional

# Frontend unit tests
cd frontend && npm run test

# Frontend tests with coverage
cd frontend && npm run test:coverage
```

## Linting and formatting

```bash
# Python
uv run ruff check --fix .
uv run ruff format .
uv run mypy --config-file .mypy.ini --non-interactive

# Frontend
cd frontend && npm run lint
cd frontend && npm run typecheck
```

## Releasing a new version

```bash
uv run cz bump        # bumps pyproject.toml, __init__.py, frontend/package.json, generates CHANGELOG.md
git push --follow-tags
```
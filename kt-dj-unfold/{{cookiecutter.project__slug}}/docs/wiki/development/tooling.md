# Tooling Guide

## Essential Tools

{{ cookiecutter.project__name }} uses a modern Python toolchain optimized for developer experience and code quality.

### 1. UV - Package Manager

**Purpose**: Install dependencies, manage virtual environments, install Python binaries.

**Why UV?**
- 10-100x faster than pip
- Single tool for venvs + packages + Python installation
- Optimized lockfile generation
- Modern dependency resolution

**Common Commands**:

```bash
# Create virtual environment
uv venv

# Install all dependencies from pyproject.toml
uv sync

# Add a new dependency
uv add package-name

# Add dev/test dependencies
uv add --group dev package-name
uv add --group test package-name

# Update dependencies
uv sync --refresh

# Show dependency tree
uv tree

# Check for outdated packages
uv pip list --outdated
```

**Configuration** (`pyproject.toml`):

```toml
[tool.uv]
default-groups = [ "dev", "test", "docs" ]
package = true  # Enables `uv build`
```

### 2. Ruff - Linter & Formatter

**Purpose**: Fast Python linter and formatter (replaces Flake8, pycodestyle, etc.).

**Why Ruff?**
- Extremely fast (Rust-based)
- Single tool for linting and formatting
- Hundreds of rules including Django-specific
- IDE integration available

**Configuration** (`ruff.toml`):

```toml
target-version = "py314"
line-length = 150

[lint]
select = ["A", "ANN", "DJ", "S", ...]  # See full list in ruff.toml
ignore = ["D100", "D104", ...]           # Docstring exemptions
```

**Common Commands**:

```bash
# Check all files for issues
ruff check .

# Format all Python files
ruff format

# Fix auto-fixable issues
ruff check . --fix

# Run on specific file
ruff check src/{{ cookiecutter.project__slug }}/config/settings.py

# Preview changes without applying
ruff format --diff .
```

**Pre-commit Hook**:

```yaml
- repo: https://github.com/charliermarsh/ruff-pre-commit
  rev: 'v0.11.7'
  hooks:
    - id: ruff
```

### 3. Pre-commit

**Purpose**: Run checks before committing code.

**Why Pre-commit?**
- Catches issues before code review
- Enforces consistency across contributors
- Runs same checks locally and CI

**Configuration** (`.pre-commit-config.yaml`):

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: debug-statements
  
  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: 'v0.11.7'
    hooks:
      - id: ruff
  
  - repo: https://github.com/saxix/pch
    rev: '0.1'
    hooks:
      - id: check-missed-migrations
      - id: check-version-release-match
```

**Common Commands**:

```bash
# Run all pre-commit hooks on staged files
pre-commit run

# Run all hooks on all files (full check)
pre-commit run --all-files

# Install git hooks
pre-commit install
```

### 4. pytest - Testing Framework

**Purpose**: Python testing framework with extensive ecosystem.

**Why pytest?**
- Simple, intuitive syntax
- Powerful fixtures and parametrization
- Rich plugin ecosystem
- Excellent error messages

**Configuration** (`pytest.ini`):

```ini
[pytest]
 DJANGO_SETTINGS_MODULE = {{ cookiecutter.project__slug }}.config.settings
```

**Common Commands**:

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_models.py

# Run with coverage
pytest --cov={{ cookiecutter.project__slug }} --cov-report=term-missing

# Run with verbose output
pytest -v

# Run only failed tests (requires pytest-rerunfailures)
pytest --lf
```

**Test Structure** (`tests/`):

```python
# tests/__init__.py
# tests/test_z.py  # Example test file
```

### 5. Hatch - Build System

**Purpose**: Python packaging and distribution.

**Why Hatch?**
- Modern, configuration-driven
- Plugins for versioning (hatch-vcs)
- Clean project layout support
- Building sdist/wheels

**Configuration** (`pyproject.toml`):

```toml
[build-system]
requires = ["hatchling>=1.25", "hatch-vcs>=0.4"]
build-backend = "hatchling.build"

[tool.hatch.version]
source = "vcs"
```

**Common Commands**:

```bash
# Build package (creates dist/)
uv build

# Install in editable mode (for development)
pip install -e .

# Show package info
uv pip show {{ cookiecutter.project__slug }}
```

### 6. Django CLI Tools

**Purpose**: Development and deployment tasks.

**Key Commands**:

```bash
# Run development server
./manage.py runserver

# Apply database migrations
./manage.py migrate

# Create new migration
./manage.py makemigrations app_name

# Create superuser
./manage.py createsuperuser

# Upgrade project (migrate + collectstatic)
./manage.py upgrade --no-input --migrate --static

# Demo data setup
./manage.py demo

# Collect static files
./manage.py collectstatic
```

**Custom Commands** (`src/{{ cookiecutter.project__slug }}/management/commands/`):

```python
# src/{{ cookiecutter.project__slug }}/management/commands/upgrade.py
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = " Upgrade project: migrate + collectstatic + create superuser"
```

### 7. Docker & Container Tools

**Purpose**: Containerized development and deployment.

**Docker Commands**:

```bash
# Build image
docker build -t {{ cookiecutter.project__slug }} .

# Run container (dev mode)
docker run -p 8000:8000 {{ cookiecutter.project__slug }} dev

# Run container (production mode)
docker run -p 8000:8000 {{ cookiecutter.project__slug }} run

# Run worker
docker run {{ cookiecutter.project__slug }} worker
```

**Entry Point** (`docker/etc/entrypoint.sh`):

```bash
dev)      # Development server
run)      # uWSGI production
worker)   # Celery worker
beat)     # Celery beat scheduler
flower)   # Celery monitoring
```

### 7a. Docker Development Workflow

For containerized development and deployment.

**Setup:**
```bash
# Set registry credentials (required)
export DOCKER_REGISTRY=your-registry.com
export DOCKER_USR=your-username
export DOCKER_PWD=your-password

# Build base image (dependencies only, rarely changes)
make -C docker build-base

# Build application image
make -C docker build

# Run locally with HTTP
make -C docker run

# Or with HTTPS
make -C docker runs
```

**Image Structure:**
- Base image: Uses `docker/Dockerfile.base` with Python dependencies
- Application image: Uses `docker/Dockerfile`, depends on base image
- User: `{{ cookiecutter.project__slug }}` (non-root)
- Volume mounts: `/data/static`, `/data/media`

**Environment Variables in Container:**
Required: `DJANGO_SETTINGS_MODULE`, `DEBUG`, `DATABASE_URL`, `SECRET_KEY`, `ADMIN_*`
Optional: `SENTRY_DSN`, `ENVIRONMENT`, `STACK_PROTOCOL`

### 8. Documentation Tools

**Purpose**: Generate and maintain documentation.

**MKDocs Configuration** (`mkdocs.yml`):

```yaml
site_name: {{ cookiecutter.project__name }}
theme: material
plugins:
  - awesome-pages
  - click
```

**Common Commands**:

```bash
# Build documentation
mkdocs build

# Serve documentation locally
mkdocs serve

# Deploy to GitHub Pages
mkdocs gh-deploy
```

### 9. Security Tools

**detect-secrets**

Purpose: Prevent committing secrets.

```bash
# Initialize baseline
detect-secrets scan > .secrets.baseline

# Scan for new secrets
detect-secrets scan --baseline .secrets.baseline
```

**Configuration** (`.pre-commit-config.yaml`):

```yaml
- repo: https://github.com/Yelp/detect-secrets
  rev: v1.5.0
  hooks:
    - id: detect-secrets
      args: ['--baseline', '.secrets.baseline']
```

### 10. Environment Management

**direnv (Optional)**

Purpose: Automatic environment configuration.

```bash
# Install direnv
# Add to .bashrc or .zshrc: eval "$(direnv hook bash)"

# Allow project environment
mkdir -p ~/.config/direnv
echo 'source ~/PROJS/KT/{{ cookiecutter.project__slug }}/.env' > .envrc
direnv allow
```

**Manual Activation**:

```bash
source .venv/bin/activate  # If not using direnv
```

## Development Workflow

### Setting Up a New Project

```bash
# Clone repository
git clone https://github.com/k-tech-italy/{{ cookiecutter.project__slug }}.git

# Install dependencies (creates .venv)
uv sync

# Setup environment file
cp .env.example .env
# Edit .env with your configuration

# Setup database (if using Postgres)
psql -U postgres -d {{ cookiecutter.project__slug }} -c "CREATE DATABASE {{ cookiecutter.project__slug }};"

# Run upgrade to migrate + create superuser
./manage.py upgrade --no-input \
  --admin-email admin@example.com \
  --admin-username admin \
  --admin-password password

# Install pre-commit hooks
pre-commit install
```

### Daily Development

```bash
# Run linters (before commit)
ruff check .
ruff format .

# Or use pre-commit (staged files only)
pre-commit run

# Run tests (before push)
pytest

# Run full linting check
tox -e lint  # or make lint
```

### Adding New Dependencies

```bash
# Add production dependency
uv add django-new-package

# Add dev dependency
uv add --group dev pytest-new-plugin

# Add test dependency
uv add --group test factory-boy

# Remove dependency
uv remove package-name

# Update all dependencies
uv sync --refresh

# Update specific package
uv upgrade package-name
```

### Running Commands in Container

```bash
# Run management command in container
docker exec -it <container> ./manage.py shell

# Run database migration in container
docker exec -it <container> ./manage.py migrate

# Access container shell
docker exec -it <container> bash
```

## Tool Integration Matrix

| Task | Primary Tool | Alternative |
|------|-------------|-------------|
| Dependency Management | UV | pip, poetry |
| Packaging | Hatchling | setuptools |
| Versioning | hatch-vcs | setuptools-scm, dumbversion |
| Linting | Ruff | Flake8, Pylint |
| Formatting | Ruff | Black, autopep8 |
| Testing | pytest | unittest |
| Documentation | MKDocs | Sphinx |
| Security Scanning | detect-secrets | truffleHog, gitleaks |
| Virtual Environments | UV | venv, conda |

## VSCode Integrated Development Environment

**Recommended Extensions**:

1. **Python** (ms-python.python)
2. **Ruff** (charliermarsh.ruff)
3. **Pylance** (ms-python.pylance)
4. **GitLens** (eamodio.gitlens)
5. **EditorConfig** (editorconfig.editorconfig)

**Recommended Settings** (`.vscode/settings.json`):

```json
{
  "python.defaultInterpreterPath": ".venv/bin/python",
  "python.linting.enabled": true,
  "python.formatting.provider": "ruff",
  "ruff.lint.args": ["--select=ALL"],
  "files.eol": "\n",
  "editor.tabSize": 4,
  "editor.insertSpaces": true
}

## Makefile Commands Reference

### Main Makefile (root directory)

The root `Makefile` provides common development tasks with discoverable help.

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
| `make outdated` | Generate dependency outdated reports |

### Docker Makefile (`docker/Makefile`)

For containerized development and deployment. Requires registry credentials.

**Prerequisites:**
- Set `DOCKER_REGISTRY`, `DOCKER_USR`, `DOCKER_PWD`
- Optional: `ECR_AWS_PROFILE`, `ECR_AWS_REGION` for AWS ECR

| Target | Description |
|--------|-------------|
| `make help` | Show available docker targets |
| `make build-base` | Build base image with dependencies |
| `make build` | Build application image |
| `make registrylogin` | Log in to Docker registry (ECR or custom) |
| `make release` | Push image to registry |
| `make release-latest` | Tag and push as latest version |
| `make full-release` | Build and release everything |
| `make run` | Run container with HTTP (port 8000) |
| `make runs` | Run container with HTTPS (port 443) |
| `make shell` | Open container interactive shell |
| `make test` | Run Django health checks in container |
| `make stack` | Run web + Celery services together |

### Environment Variables

**Root Makefile:**
- `NODE_ENV` - Node environment for webpack (default: production)

**Docker Makefile:**
- `DOCKER_REGISTRY` - Docker registry URL (required)
- `STACK_PROTOCOL` - HTTP or HTTPS (default: https)
- `LOCAL_PORT`, `LOCAL_HTTPS_PORT` - Container port mappings

## Version Management

The project uses `hatch-vcs` to manage versions from Git tags.

### Workflow

```bash
# Increment version (creates commit but doesn't push)
make bump

# Options: major / minor / patch
# Example output:
# bumpversion [major/minor/patch]: patch

# After review and merge, tag the release
git tag v0.1.2  # or appropriate version

# Push tags
git push --tags
```

### Version Format

- Versions come from Git tags: `vX.Y.Z`
- Development versions: `X.Y.Z.devN` (until tag)
- Automatically written to `src/{{ cookiecutter.project__slug }}/version.py` on build

### Makefile Integration

```makefile
bump:   ## Bumps version
    bumpversion [major|minor|patch]
```

Uses `.bumpversion.cfg` configuration for automated version updates across files.
```

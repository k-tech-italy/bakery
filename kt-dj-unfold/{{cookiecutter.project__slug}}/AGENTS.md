# {{ cookiecutter.project__name }} Project Context

## Quick Start

This is **{{ cookiecutter.project__name }}** - a Django project scaffolding with Django-Unfold as the admin interface.

## Documentation Overview

All project context and development guidelines are documented under `docs/`:

### For AI Agents
- **[wiki/development/structure.md](../docs/wiki/development/structure.md)** - Project structure, configuration patterns, Makefile targets
- **[wiki/development/principles.md](../docs/wiki/development/principles.md)** - Development principles, security standards, testing requirements
- **[wiki/development/design_decisions.md](../docs/wiki/development/design_decisions.md)** - Architecture rationale (Unfold, configuration fragments, Hatch-VCS)
- **[wiki/development/tooling.md](../docs/wiki/development/tooling.md)** - UV, Ruff, pytest, Makefiles, Docker workflows

### For Developers
Start with `CONTRIBUTING.md` for setup instructions.

## Environment Setup

```bash
# Prerequisites: UV package manager
uv sync

# Run migrations and create superuser
./manage.py upgrade --no-input \
  --admin-email admin@example.com \
  --admin-username admin \
  --admin-password password
```

## Key Technologies

- **Framework**: Django 6+ with Python 3.14+
- **Admin**: Django-Unfold
- **Package Manager**: UV
- **Linting**: Ruff (with pre-commit hooks)
- **Testing**: pytest
- **Versioning**: hatch-vcs (from Git tags)

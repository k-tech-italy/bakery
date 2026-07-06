# Design Decisions

## Rationale Behind Key Architecture Choices

### 1. Why Django-Unfold Instead of Standard Admin?

**Decision**: Use [Django-Unfold](https://unfoldadmin.com) as the admin interface.

**Rationale**:

- **Modern UI/UX**: Unfold provides a cleaner, more intuitive interface than Django's default admin
- **Customization**: Easy theme customization with environment badges and branding
- **Extensibility**: Plugins for constance, import-export, guardian, simple-history
- **Performance**: Better performance characteristics with modern front-end stack

**Implementation** (`src/{{ cookiecutter.project__slug }}/config/fragments/unfold.py`):

```python
UNFOLD = {
    "SITE_TITLE": "{{ cookiecutter.project__name }}",
    "ENVIRONMENT": get_environment,  # Visual environment indicator
    "COMMAND": {                     # Enhanced search and commands
        "search_models": True,
        "show_history": True,
    },
}
```

### 2. Why Configuration Fragments?

**Decision**: Split Django settings into modular fragments instead of a single monolithic file.

**Rationale**:

- **Separation of Concerns**: Each fragment handles one aspect (security, logging, admin)
- **Reusability**: Fragments can be shared across projects
- **Maintainability**: Easier to find and update specific settings
- **Testing**: Individual fragments can be tested in isolation

**Pattern**:

```python
# settings.py
from .fragments.security import *  # noqa: F401,F403
from .fragments.unfold import *    # noqa: F401,F403

# Fragment file (e.g., security.py)
SECURE_HSTS_SECONDS = _env('SECURE_HSTS_SECONDS')
CSRF_COOKIE_SECURE = True
```

### 3. Why Hatch-VCS for Versioning?

**Decision**: Use `hatch-vcs` instead of hardcoded versions or manual management.

**Rationale**:

- **Source of Truth**: Version comes from Git tags, not files
- **Automation**: No manual version bumping required
- **Consistency**: Same version across all artifacts
- **CI/CD Friendly**: Works seamlessly with automated pipelines

**Trade-offs**:

- Requires tag creation for releases
- Cannot modify version manually (must use `make bump`)
- Needs `.git` directory for builds

### 4. Why UV as Package Manager?

**Decision**: Use [UV](https://github.com/astral-sh/uv) instead of pip/pip-tools.

**Rationale**:

- **Speed**: UV is significantly faster than pip (10-100x)
- **Single Tool**: Manages packages, venvs, and Python installations
- **Lockfile Quality**: Produces highly optimized lockfiles
- **Modern Ecosystem**: Built with modern Python packaging standards

**Configuration** (`pyproject.toml`):

```toml
[tool.uv]
default-groups = [ "dev", "test", "docs" ]
package = true  # Build package from source
```

### 5. Why Feature Flags?

**Decision**: Integrate [django-flags](https://github.com/caktus/django-flags) for feature management.

**Rationale**:

- **Gradual Rollout**: Release features incrementally
- **Testing**:_enable features like Django Debug Toolbar for specific users/environments
- **Disabling**: Kill switches for problematic features
- **A/B Testing**: Foundation for experiments

**Usage**:

```python
# settings.py
FLAGS = {
    'DDT_ENABLE': [],  # Debug toolbar flag
}

# In code
if flag_enabled('FEATURE_NAME'):
    # Enable feature
```

### 6. Why Pre-commit Hooks?

**Decision**: Enforce code quality via pre-commit hooks.

**Rationale**:

- **Consistency**: All developers use the same linters
- **Early Detection**: Catch issues before review
- **Automated Checks**: Detect-migrations, secrets, formatting
- **Standards Enforcement**: No manual enforcement needed

**Hooks** (`.pre-commit-config.yaml`):

```yaml
hooks:
  - id: ruff                    # Linting
  - id: detect-secrets         # Security scanning
  - id: check-missed-migrations # Django migrations
  - id: compilemessages        # i18n files
```

### 7. Why Dynamic Configuration (Django-Constance)?

**Decision**: Use [django-constance](https://github.com/jazzband/django-constance) for runtime configuration.

**Rationale**:

- **No Deploys Required**: Change settings without redeploying
- **Database Storage**: Persist values across instances
- **Admin Interface**: Non-developers can modify settings
- **Type Safety**: Add custom form fields

**Configuration** (`constance.py`):

```python
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
```

### 8. Why Sentry Integration?

**Decision**: Integrate [Sentry](https://sentry.io) for error tracking.

**Rationale**:

- **Immediate Awareness**: Get notified when errors occur
- **Context**: See Full stack traces, user data, and environment
- **Release Tracking**: Link errors to specific versions
- **Debugging**: Reproduce issues with detailed breadcrumbs

**Setup** (`fragments/sentry.py`):

```python
sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[DjangoIntegration(), sentry_logging],
    release=__version__,
    environment=_env('ENVIRONMENT'),
)
```

### 9. Why Directory-Based Templates?

**Decision**: Organize templates by app (`src/{{ cookiecutter.project__slug }}/web/templates/`).

**Rationale**:

- **Discovery**: Find all web templates easily
- **Separation**: Web templates separate from admin templates
- **Simplicity**: Flat structure for small projects
- **Flexibility**: Easy to add new template directories

**Template Loading** (`settings.py`):

```python
TEMPLATES = [{
    "DIRS": [os.path.join(BASE_DIR, "web/templates")],
}]
```

### 10. Why Makefile?

**Decision**: Use `Makefile` for common tasks instead of shell scripts.

**Rationale**:

- **Discoverability**: `make help` shows all available targets with inline documentation
- **Abstraction**: Hide complex commands behind simple, memorable targets
- **Cross-platform**: Works identically on Linux/macOS/WSL without special shells
- **Integration**: Seamlessly integrate UV, pre-commit, pytest, and Docker workflows
- **Documentation**: Self-documenting via `##` comments parsed by PRINT_HELP_PYSCRIPT

**Makefile Structure:**

The project uses two Makefiles for different contexts:

**Root Makefile (`Makefile`):**
```makefile
develop:  ## Initialize project (git, venv, env files)
static:   ## Build static assets (Sass/webpack + collectstatic)
lint:     ## Run pre-commit hooks on all files
test:     ## Run pytest test suite
bump:     ## Increment version (major/minor/patch)

# Help system - auto-generated from comments
help:     ## Show this help message
```

**Docker Makefile (`docker/Makefile`):**
```makefile
build-base:  ## Build base image with dependencies
build:       ## Build application image
release:     ## Push to Docker registry
run:         ## Run container locally (HTTP)
runs:        ## Run container locally (HTTPS)

# Help system
help:        ## Show docker targets
```

**Features:**
-guard-% pattern ensures required environment variables are set
- PRINT_HELP_PYSCRIPT auto-parses `##` comments for help documentation
- Separate Makefiles keep concerns isolated (dev vs deployment)

## Architectural Trade-offs

### Explicit Environment Variables vs Defaults

**Decision**: Require all critical configuration via environment variables.

**Trade-off**: More setup required initially, but prevents environment-specific bugs.

### Modular Settings vs Single File

**Decision**: Split settings into fragments.

**Trade-off**: More files to navigate, but better organization and reusability.

### Hatch-VCS Versioning vs Manual

**Decision**: Auto-generate version from Git.

**Trade-off**: Cannot edit version file manually, but ensures consistency.

## Evolutionary Decisions

These decisions evolved based on:

1. **Problems encountered** in previous Django projects
2. **Industry best practices** (Django security checklist, etc.)
3. **Team preferences** for modern tooling
4. **Deployment requirements** (Docker, CI/CD)

## Anti-Patterns Avoided

- ❌ Hardcoded configuration values
- ❌ Monolithic settings.py (>500 lines)
- ❌ Manual version management
- ❌ Multiple package managers (pip + conda, etc.)
- ❌ Secrets in code or config files
- ❌ Unittest over pytest
- ❌ Inline CSS/JavaScript

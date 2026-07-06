# Development Principles

## Core Philosophy

{{ cookiecutter.project__name }} follows these guiding principles for all code contributions:

### 1. Production-Ready by Default

- Code should be deployable to production at any time
- Security is non-negotiable (see Security section)
- Default configurations should follow Django security best practices
- Environment-specific settings are isolated in configuration fragments

### 2. Explicit Over Implicit

- Configuration values come from environment variables, not hardcoded defaults
- Use `{{ cookiecutter.project__slug }}.config.env()` for all configuration reads
- Document all environment variables in `.env.example`
- Avoid implicit assumptions about runtime state

### 3. Modular Configuration

- Settings are organized into reusable fragments
- Fragments can be enabled/disabled per deployment
- Follow the pattern: `fragment.py` + import in `settings.py`

### 4. Version Control first

- All code changes go through git
- Use semantic versioning (SemVer)
- Version is managed automatically via `hatch-vcs`
- Never manually edit `src/{{ cookiecutter.project__slug }}/version.py`

## Security Principles

### 1. Defense in Depth

```python
# Example from security.py fragment
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = SECURE_SSL_REDIRECT
SESSION_COOKIE_HTTPONLY = True
```

- Multiple layers of protection (SSL, CSRF, XSS prevention)
- Cookies marked as secure and HTTP-only
- CSP headers configured

### 2. Secrets Management

- **NEVER** commit secrets or keys
- Use environment variables for all sensitive data
- Run `make detect-secrets` before pushing
- Secrets baseline managed in `.secrets.baseline`

### 3. Environment Detection

```python
# From unfold.py fragment
def get_environment(request):
    environ = env("ENVIRONMENT").upper()
    if environ == "LOCAL":
        return [environ, "success"]
    elif environ.startswith("PROD"):
        return ["PROD", "danger"]
    # ...
```

- Visual indicators for different environments
- Prevents accidental actions in wrong environment

## Code Quality Standards

### 1. Testing Requirements

```python
# From CONTRIBUTING.md
You **must** make sure that your changes are covered by unit and integration tests.
```

- All new features require tests
- Integration tests cover critical paths
- Test coverage tracked via pytest-cov

### 2. Linting Enforcement

```toml
# From ruff.toml
select = [
    "A",   # prevent using keywords that clobber python builtins
    "ANN", # flake8 annotations
    "DJ",  # flake8-django
    "S",   # bandit (security)
    # ...
]
```

- Pre-commit hooks run ruff on all files
- 150-character line length for readability
- Django-specific linting rules enabled

### 3. Documentation

- Docstrings required for public APIs
- README updates for new features
- Configuration changes documented in `.env.example`

## Git Workflow

### Branching Strategy

```
main          → Production-ready code
develop       → Integration branch
feature/*     → New features (short-lived)
hotfix/*      → Critical production fixes
release/*     → Release preparation
```

### Commit Guidelines

- Atomic commits with clear messages
- Reference issues: `Fixes #123`
- Use present tense: "Add feature" not "Added feature"

### Pull Request Process

1. Fork the repository
2. Create a feature branch from `develop`
3. Make changes following these principles
4. Add tests for new functionality
5. Ensure all checks pass (tests, linting)
6. Submit PR with clear description

## Dependency Management

### Package Manager: UV

```toml
# From pyproject.toml
[tool.uv]
default-groups = [ "dev", "test", "docs" ]
package = true
```

- **Single source of truth**: `pyproject.toml`
- **Lock file**: `uv.lock` (commit changes)
- **Virtual environments**: Managed by UV

### Dependency Principles

1. Pin exact versions in lockfile
2. Use semantic versioning in pyproject.toml
3. Group dependencies logically (dev, test, docs, image)
4. Update dependencies regularly via UV

## Releasing Process

```bash
# From CONTRIBUTING.md
Versioning uses SemVer via VCS tags.
When building the package `uv build` it will write the version to src/{{ cookiecutter.project__slug }}/version.py.

# Bump version (local, not committed)
make bump  # then choose major/minor/patch
```

### Release Steps

1. Ensure all changes are merged to `develop`
2. Update CHANGELOG if applicable
3. Run `make bump` to increment version
4. Create pull request for version update
5. Merge to `main` (triggers CI release)
6. Tag the release commit

## Error Handling & Monitoring

### Sentry Integration

```python
# From sentry.py
def capture_exception(error=None):
    return _capture_exception(error)

def crashlog_process_exception(exception, request=None, message_user=False):
    return _capture_exception(exception)
```

- All exceptions captured in Sentry
- Release version tracked with errors
- Environment tagged for filtering

## Performance Considerations

1. Database: Use `select_related`/`prefetch_related` for queries
2. Caching: Implement caching for expensive operations
3. Static files: Minified and compressed in production
4. Media: Offloaded to CDN in production

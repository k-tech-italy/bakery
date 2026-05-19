# AGENTS.md — cookiecutter-django-react (template maintainer guide)

Rules for AI coding agents maintaining or extending this cookiecutter template.

---

## Repository layout

```
cookiecutter-django-react/
├── cookiecutter.json                         # all template variables + defaults
├── hooks/
│   ├── pre_gen_project.py                    # input validation (slug, package, app name)
│   └── post_gen_project.py                   # conditional file removal; NO installs/git
└── {{cookiecutter.project_slug}}/            # rendered output lives here
    └── ...                                   # every file is a Jinja2 template
```

---

## Cookiecutter variables (`cookiecutter.json`)

| Key | Type | Values | Notes |
|---|---|---|---|
| `project_name` | str | free | Human-readable; used in README, mkdocs.yml, Navbar |
| `project_slug` | str | `^[a-z][a-z0-9-]+$` | Repo name, Docker image prefix, validated in pre_gen hook |
| `package_name` | str | `^[a-z][a-z0-9_]+$` | Python package; Docker system user; validated in pre_gen hook |
| `first_app_name` | str | `^[a-z][a-z0-9_]+$` | First Django app; validated in pre_gen hook |
| `description` | str | free | Shown in README, mkdocs, pyproject description |
| `author_name` | str | free | LICENSE and pyproject.toml |
| `author_email` | str | free | pyproject.toml |
| `year` | str | `"2026"` | Copyright year in LICENSE; update the default each year |
| `python_version` | str | `"3.13"` | `.python-version`, Dockerfile FROM, ruff target-version |
| `django_version` | str | `"5.2"` | Pinned in pyproject.toml |
| `postgres_version` | str | `"17"` | postgres image tag in docker-compose |
| `redis_version` | str | `"8"` | redis image tag; only used when `use_celery == "yes"` |
| `use_celery` | choice | `["yes", "no"]` | Gates: celery.py, Redis service, worker service, test fixtures |
| `use_sentry` | choice | `["yes", "no"]` | Gates: sentry-sdk dep, Sentry init block in settings.py |
| `use_mkdocs` | choice | `["yes", "no"]` | Gates: docs/ directory, mkdocs.yml, docs.yml workflow |
| `use_trivy` | choice | `["yes", "no"]` | Gates: trivy scan steps inside `docker.yml`, `.trivyignore` (the workflow itself always exists for the `publish` job) |
| `open_source_license` | choice | `["MIT", "Apache-2.0", "none"]` | Gates: LICENSE file content |

---

## Jinja2 rendering rules

### Basic substitution
```
{{ cookiecutter.project_name }}
{{ cookiecutter.package_name }}
{{ cookiecutter.first_app_name }}
```

### Conditional blocks
```
{% if cookiecutter.use_celery == "yes" %}
...celery-specific content...
{% endif %}
```

### String filters
```
{{ cookiecutter.first_app_name | capitalize }}   →  Core
{{ cookiecutter.package_name | upper }}          →  MYPROJECT
```

### Current year in LICENSE
Uses `cookiecutter-extensions`:
```
{% now 'utc', '%Y' %}
```

### GitHub Actions escaping (CRITICAL)
GitHub Actions uses `${{ variable }}` which conflicts with Jinja2. Escape like this:
```yaml
# In any .github/workflows/*.yml template file:
${{ '{{' }} github.workflow {{ '}}' }}
${{ '{{' }} matrix.python-version {{ '}}' }}
```
This renders to `${{ github.workflow }}` in the output file.

---

## Adding a new feature toggle

1. Add the variable to `cookiecutter.json` as a choice list, e.g.:
   ```json
   "use_myfeature": ["yes", "no"]
   ```
2. Create any feature-specific template files under `{{cookiecutter.project_slug}}/`.
3. Wrap feature-specific content in existing files with:
   ```
   {% if cookiecutter.use_myfeature == "yes" %}
   ...
   {% endif %}
   ```
4. Add removal logic to `hooks/post_gen_project.py`:
   ```python
   if "{{ cookiecutter.use_myfeature }}" != "yes":
       _remove("path/to/feature_file.py")
       _remove("path/to/feature_dir/")
   ```
5. Update this AGENTS.md variable table.
6. Update the template-root `README.md` variable table.

---

## Updating pinned versions

When bumping a dependency version (Django, postgres, node, etc.):

1. Find all occurrences: `grep -r "5\.2" {{cookiecutter.project_slug}}/` (for Django 5.2).
2. Update in: `cookiecutter.json` default, `pyproject.toml`, Dockerfiles, `docker-compose.yml`,
   README.md, CONTRIBUTING.md, AGENTS.md (generated project).
3. Prefer updating the `cookiecutter.json` default so new projects get the new version
   automatically while existing projects are unaffected.

---

## `hooks/pre_gen_project.py` rules

- Validate `project_slug` matches `^[a-z][a-z0-9-]+$`.
- Validate `package_name` matches `^[a-z][a-z0-9_]+$`.
- Validate `first_app_name` matches `^[a-z][a-z0-9_]+$`.
- On failure: `print(...)` then `sys.exit(1)`.

---

## `hooks/post_gen_project.py` rules

- **Only** do conditional file/directory removal and print a pointer to CONTRIBUTING.md.
- **No** `git init`, `git commit`, `uv sync`, `npm install`, or any install command.
  Those belong in CONTRIBUTING.md (developer responsibility, not cookiecutter's).
- Use a helper `_remove(path)` that handles both files and directories.
- Exit cleanly (no exception) even when optional files are absent.

---

## Testing the template

```bash
# Generate into a temp dir
cookiecutter . --output-dir /tmp/cc-test --no-input

# Verify backend starts
cd /tmp/cc-test/my-project
uv sync
cp .env.example .env
uv run manage.py check

# Verify frontend builds
cd frontend && npm install && npm run build && npm run test
```

For a full end-to-end smoke test with all options enabled:
```bash
cookiecutter . --output-dir /tmp/cc-full \
  use_celery=yes use_sentry=yes use_mkdocs=yes use_trivy=yes \
  open_source_license=MIT
```

---

## What NOT to add to the template

- Generated files (`uv.lock`, `package-lock.json`, `CHANGELOG.md`, `.secrets.baseline`) —
  these are produced after project creation.
- Project-specific business logic — keep the first app as a minimal stub.
- Opinionated third-party packages beyond the established stack — add them to the generated
  project's CONTRIBUTING.md as optional instructions instead.
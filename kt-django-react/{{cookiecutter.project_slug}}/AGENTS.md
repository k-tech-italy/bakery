# AGENTS.md — {{ cookiecutter.project_name }}

Conventions and rules for AI coding agents (Claude, Copilot, Cursor, etc.) working in this
repository. Read this file before making changes. Rules here override general knowledge and
defaults.

---

## Python / uv

- Manage deps with `uv add` / `uv remove`; never edit `uv.lock` by hand.
- Dep groups: no group = runtime; `dev` = test + debug; `checks` = lint; `deployment` = uWSGI
  etc.; `docs` = mkdocs (if enabled).
- In CI use `uv sync --frozen`; locally `uv sync` is fine.
- Run any command inside the venv with `uv run <cmd>` — never activate the venv manually.

---

## Django

- All settings come from environment variables via `django-environ`; never use `os.environ`
  directly.
- `INSTALLED_APPS` follows the four-section pattern: DEFAULT → THIRDPARTY → USER → LOCAL.
- Each app owns an `api/` sub-package: `serializers.py`, `views.py`, `urls.py`, `openapi.py`.
- Authentication: `TokenAuthentication` + `SessionAuthentication`; permissions:
  `DjangoModelPermissions`; pagination: `PageNumberPagination(page_size=10)`.
- API schema via `drf-spectacular` with `COMPONENT_SPLIT_REQUEST = True`; custom tags and
  postprocessing hooks live in the app's `api/openapi.py`.
- The `upgrade` management command (check → collectstatic → migrate →
  remove_stale_contenttypes → createsuperuser → per-app init commands) must be idempotent;
  run it on every deploy. **Always verify changes by running `upgrade`, never individual commands.**
- Each app that needs seed data owns an `init_<app>` management command; `upgrade` calls them
  in order after migrations.
- Seed data lives in `<app>/data/<name>.csv`. Init commands use `get_or_create` — never
  `update_or_create` — so manual edits made through the UI are never overwritten.
- Never edit migration files by hand; always use `makemigrations` after model changes.
- Always use `user.set_password(raw) + user.save()` to hash passwords. Never
  `User.objects.update(password=raw)` — that stores plaintext and breaks authentication.
- `django_stubs_ext.monkeypatch()` is called at the top of `settings.py`. Django classes are
  therefore subscriptable at runtime — use `ModelAdmin[MyModel]` syntax freely; never add
  `# type: ignore[type-arg]` to work around missing type arguments.

---

## API versioning

Versioning is applied **per resource at router registration**, not as a top-level URL prefix.
The version suffix is part of the router prefix:

```python
# api/urls.py
router = routers.DefaultRouter()
router.register(r"projects/v1", ProjectViewSet, basename="project")
router.register(r"file-annotations/v1", FileAnnotationViewSet, basename="file-annotation")
```

This yields routes like `/api/{{ cookiecutter.first_app_name }}/projects/v1/`.
Point-auth endpoints follow the same convention: `api/auth/token/v1/`.

Rules:
- To introduce a breaking change, register the new viewset alongside the old one:
  `router.register(r"projects/v2", ProjectV2ViewSet, basename="project-v2")`.
  The `v1` routes remain live; remove them only after all clients have migrated.
- Never rename or reuse an existing version prefix — treat published routes as immutable.
- New non-breaking fields on existing serializers do not require a version bump.

---

## Celery (if enabled)

- App defined in `config/celery.py`; imported at package root `__init__.py`.
- Always set `CELERY_TASK_TRACK_STARTED = True`.
- Task arguments must be primitives (str, int, …) — never pass model instances.
- **NEVER use `CELERY_TASK_ALWAYS_EAGER` / `task_always_eager`.** It was deprecated in
  Celery 4 and removed in intent for Celery 5. It hides real serialisation and routing bugs.
- **Correct test pattern**: use `celery.contrib.pytest` fixtures (`celery_app`,
  `celery_worker`) with `broker_url: "memory://"` and `result_backend: "cache+memory://"`.
  This spins up a real in-process worker without needing Redis. See
  `tests/_extras/test_utils/celery.py`.
- Unit tests that only assert task logic: call `.apply()` directly (no worker needed).
- Functional / integration tests that need DB or filesystem side-effects: use the
  `run_celery_task_in_background` context manager from `test_utils.celery`.
- Task test pattern: `result = my_task.delay(arg); assert result.get(timeout=10) == expected`

---

## Testing (Python)

- `tests/unit/` — fast, no external deps; `tests/functional/` — DB + browser;
  `tests/integration/` — cross-component.
- Shared fixtures in `tests/conftest.py`: `api_client`, `admin_user`, `regular_user`,
  `authenticated_client`, `api_admin_client`, `tmp_media_root`.
- For Django admin view tests use pytest-django's built-in `admin_client` fixture (session-based
  Django `Client`). For REST API tests use `api_admin_client` (token-based `APIClient`).
  Do not confuse the two — the project intentionally keeps them under different names.
- Celery fixtures in `tests/_extras/test_utils/celery.py`: `celery_config`, re-exported
  `celery_app`, `celery_worker`, `run_celery_task_in_background`.
- Selenium fixtures in `tests/functional/conftest.py`: `selenium_driver` (session-scoped),
  `browser` (driver + live_server), `frontend_server` (Vite preview build).
- `UserFactory` in `tests/_extras/test_utils/factories.py`; exposes `_raw_password`.
- Use `--no-functional` to skip slow browser tests locally.
- Only test logic **we wrote**. Do not write tests that only assert on Django framework
  internals (field `max_length`, `db_table`, ORM CRUD). Admin tests must be view tests
  (HTTP requests via `admin_client`), not class-attribute checks.
- Coverage gate: 70 % (fail_under). Target: 90 %.
- `--reuse-db` locally; always `--create-db` in CI.

---

## Ruff

- Target: Python {{ cookiecutter.python_version }}+; line length 120; double quotes.
- `uv run ruff check --fix . && uv run ruff format .`

---

## MyPy

- Strict mode; migrations excluded; `mypy-drf-extensions` plugin enabled.
- `uv run mypy --config-file .mypy.ini --non-interactive`

---

## Pre-commit

- Hooks: ruff, ruff-format, mypy, frontend-lint (ESLint), frontend-typecheck (tsc),
  detect-secrets, pre-commit-hooks, commitizen.
- Frontend hooks (`frontend-lint`, `frontend-typecheck`) use `language: system` and only
  run when files under `frontend/` change. They require Node and `npm install` to have been
  run inside `frontend/` before the first commit.
- `uv run pre-commit install` once after cloning.
- On demand: `uv run pre-commit run --all-files`
- Update baseline after adding new intentional patterns:
  `uv run detect-secrets scan > .secrets.baseline`

---

## Git / Commits

- Use `uv run cz commit` for an interactive conventional commit prompt that validates the
  message format and guides you through type, scope, and description.
- Direct format: `<type>(<scope>): <description>` — types: `feat`, `fix`, `docs`, `style`,
  `refactor`, `test`, `ci`, `chore`.
- Branches: `feature/<slug>` or `bugfix/<slug>` → `develop`; PR to `main`.
- Release: `uv run cz bump` — bumps `pyproject.toml`, `src/{{ cookiecutter.package_name }}/__init__.py`,
  `frontend/package.json`, generates `CHANGELOG.md`.
- Never commit `.env`; always commit `.env.example` and `.env-docker.example`.

---

## React / TypeScript

- React 19 + TypeScript strict; Vite 7; Tailwind v4 via `@tailwindcss/vite`.
- ESLint flat config: `typescript-eslint` + `react-hooks` + `react-refresh`.
- Directory conventions:
  - `components/ui/` — generic primitives (Button, Input, Modal, Spinner)
  - `components/<domain>/` — feature-specific components
  - `pages/` — route-level components named `<Thing>Page.tsx`
  - `hooks/` — `use<Thing>.ts`
  - `api/` — one file per resource + `client.ts`
  - `types/` — shared TypeScript interfaces
  - `context/` — React context providers
- All API calls go through `api/client.ts`; never raw `fetch` in components.
- Auth token stored in `localStorage`; injected via `Authorization` header in `client.ts`.

---

## Frontend unit tests (Vitest)

- `npm run test` (single run), `npm run test:watch` (dev), `npm run test:coverage`
- Test files in `src/__tests__/`, mirroring `src/`; named `*.test.tsx` / `*.test.ts`.
- `@testing-library/react` + `@testing-library/jest-dom` for DOM assertions;
  `@testing-library/user-event` for interactions.
- jsdom environment; `src/__tests__/setup.ts` imports `@testing-library/jest-dom`.
- `vitest.config.ts` is separate from `vite.config.ts` — keep concerns clean.

---

## Frontend linting

- `npm run lint` — ESLint
- `npm run typecheck` — `tsc --noEmit` (full type check, no emit)
- Both are jobs inside `.github/workflows/check.yml` (consistent grouping: all
  linting/typing in `check.yml`, all test runners in `test.yml`).

---

## Frontend version

- Single source of truth: `frontend/package.json` `"version"` field.
- `uv run cz bump` bumps it automatically via `.cz.toml` `version_files`.
- `src/constants.ts` exports `APP_VERSION` imported from `../../package.json`
  (`resolveJsonModule: true` in `tsconfig.app.json`).
- `Footer.tsx` renders `v{APP_VERSION}`; never hardcode a version string in the UI.

---

## Tailwind v4

- `@import "tailwindcss"` in `src/index.css`; no `tailwind.config.ts`.
- Use utility classes directly in TSX; `@apply` only for component-level patterns.
- Custom design tokens: `@theme { --color-*: ...; }` in `index.css`.

### Semantic CSS

Semantic CSS is **mandatory across the entire project**. The rule covers not just colors
but all visual definitions — spacing, typography, borders, radii, shadows.

**Three layers, each with a clear role:**

| Layer | What goes here | Example |
|---|---|---|
| `@theme` in `index.css` | Design tokens: colors, radii | `--color-primary`, `--radius-card` |
| `@layer components` in `index.css` | Named UI patterns | `.btn`, `.card`, `.nav-link` |
| JSX `className` | Semantic class name + one-off layout | `"btn btn-primary mt-4 w-full"` |

**`@theme` — tokens only, no raw values in components:**

```css
@theme {
  --color-primary:   oklch(54.6% 0.215 263);
  --color-danger:    oklch(57.7% 0.245  27);
  --radius-base:     0.375rem;
  --radius-card:     0.75rem;
}
```

Tokens become Tailwind utilities automatically: `bg-primary`, `rounded-card`.
Never use raw palette shades (`blue-600`, `gray-300`) or hex values anywhere in
components — not in `className`, not in `style={{}}`, not in SVG attributes.

**`@layer components` — every reusable visual pattern gets a name:**

```css
@layer components {
  .btn         { @apply inline-flex rounded-base px-3 py-1.5 text-sm font-medium …; }
  .btn-primary { @apply bg-primary text-surface hover:bg-primary-hover; }
  .card        { @apply rounded-card border border-border bg-surface shadow-sm; }
}
```

If a set of utilities describes *what something is* (a button, a card, a nav link),
it belongs here. If it describes *where something sits* in a specific layout (margin,
width, flex context unique to one usage), it can stay in JSX.

**JSX — semantic name + contextual layout only:**

```tsx
// ✅ correct
<button className="btn btn-primary mt-4 w-full">Save</button>
<article className="card p-8">…</article>

// ❌ wrong — visual recipe in the markup
<button className="inline-flex rounded-md bg-blue-600 px-3 py-2 text-sm text-white …">
```

---

## Docker

- Multi-stage builds; non-root system user (`{{ cookiecutter.package_name }}`); healthchecks
  on every service; `service_healthy` in `depends_on`.
- uWSGI binds on TCP socket; nginx upstream uses `uwsgi_pass`.
- Named volumes: `static`, `media`, `shared` (URL prefixes JSON).
- `docker/app/conf/entrypoint.sh` role=web: runs `upgrade` → `export_url_prefixes` → uwsgi.
- `docker/nginx/conf/entrypoint.sh`: reads `url_prefixes.json` to generate backend routing.
- Production install: `uv sync --no-dev --group deployment --frozen --no-editable`

---

## CI/CD (GitHub Actions)

Four workflow files — each has `cancel-in-progress: true`:

| File | Jobs |
|---|---|
| `check.yml` | `python-checks` (ruff + mypy) · `frontend-checks` (ESLint + tsc) |
| `test.yml` | `python-test` (pytest) · `frontend-test` (vitest) · `code-coverage` (Python + frontend upload to Codecov) |
| `docker.yml` | `build-and-scan` (matrix: app + nginx, optional trivy) · `publish` (push to registry on `main`/`develop`) |
| `docs.yml` | mkdocs build + GH Pages deploy (only if `use_mkdocs == "yes"`) |

- uv cache: restore → `uv sync` → save pattern.
- Node cache: `cache: 'npm'` in `setup-node` action.
- `publish` job tags: `sha-<short>` always; `latest` on `main`; `staging` on `develop`.

### Required GitHub secrets

| Secret | Description |
|---|---|
| `REGISTRY` | Registry host (e.g. `ghcr.io`, `registry.hub.docker.com`) |
| `REGISTRY_USERNAME` | Registry login username |
| `REGISTRY_PASSWORD` | Registry login password or access token |
| `CODECOV_TOKEN` | Codecov upload token (optional; upload is skipped when absent) |

---

## Security

- `detect-secrets` baseline generated once at project setup; update with
  `uv run detect-secrets scan > .secrets.baseline` after any intentional change.
- `bandit` excludes `tests/`; `trivy` scans both Docker images.
- `.trivyignore`: document each suppressed CVE with a date and reason.
- `SECRET_KEY` must always come from the environment; never hardcode it.
---
title: Management commands
---

# Management Commands

## `upgrade`

Runs all deployment steps in order. Execute on every deploy (Docker entrypoint or CI step).

### Steps

1. **check** — Django system checks (optionally with `--check-deploy` for production mode).
2. **collectstatic** — collects static files; creates `STATIC_ROOT` if absent.
3. **migrate** — applies pending migrations.
4. **remove_stale_contenttypes** — cleans up stale content types.
5. **createsuperuser** — creates a Django superuser if the username does not exist yet.

### Arguments

| Argument | Default | Env var | Description |
|---|---|---|---|
| `admin-user` | `admin` | `DJANGO_SUPERUSER_USERNAME` | Superuser username. |
| `admin-email` | — | `DJANGO_SUPERUSER_EMAIL` | Superuser email. |
| `admin-password` | — | `DJANGO_SUPERUSER_PASSWORD` | Superuser password (required on first run). |
| `verbosity` | `1` | — | Output verbosity (0–3). |

### Options

| Option | Description |
|---|---|
| `--check-deploy` | Enable Django production system checks. |

### Example

```bash
DJANGO_SUPERUSER_PASSWORD=secret python manage.py upgrade admin admin@example.com
```

---

## `export_url_prefixes`

Exports top-level URL prefixes to a JSON file. Used by the nginx entrypoint to generate the backend routing configuration.

```bash
python manage.py export_url_prefixes --output /shared/url_prefixes.json
```
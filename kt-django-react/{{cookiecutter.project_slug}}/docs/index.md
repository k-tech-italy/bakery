---
title: Home
---

# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

---

## Running with Docker

```bash
cp .env-docker.example .env-docker
# Edit .env-docker — set SECRET_KEY, ALLOWED_HOSTS, CORS_ALLOWED_ORIGINS, DJANGO_SUPERUSER_PASSWORD
docker compose up --build -d
```

The stack starts: **db** (PostgreSQL), {% if cookiecutter.use_celery == "yes" %}**redis**, **celery**, {% endif %}**app** (uWSGI), and **nginx** (reverse proxy + React frontend).

On every startup the `app` container automatically runs migrations, collects static files, and provisions the admin account.

| URL | Description |
|-----|-------------|
| `http://localhost/` | React frontend |
| `http://localhost/admin/` | Django admin |
| `http://localhost/api/schema/swagger-ui/` | Swagger UI |

---

## Further Reading

- [Management Commands](command.md)
- [Contributing](../CONTRIBUTING.md)
# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

## Stack

- **Backend**: Python {{ cookiecutter.python_version }} · Django {{ cookiecutter.django_version }} · DRF · uv
- **Frontend**: React 19 · TypeScript · Vite 7 · Tailwind v4
- **Database**: PostgreSQL {{ cookiecutter.postgres_version }}{% if cookiecutter.use_celery == "yes" %} · Redis {{ cookiecutter.redis_version }}{% endif %}
- **Deployment**: Docker Compose · uWSGI · nginx

## Quick start

See [CONTRIBUTING.md](CONTRIBUTING.md) for full setup instructions.

```bash
# Docker deployment
cp .env-docker.example .env-docker  # edit values
docker compose up --build -d
```
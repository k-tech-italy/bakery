# ── Stage 1: install Python dependencies ─────────────────────────────────────
FROM python:{{ cookiecutter.python_version }}-slim AS python-deps

WORKDIR /app

# build-essential is required to compile uwsgi from source
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock README.md ./
COPY src/ ./src/

RUN uv sync --no-dev --group deployment --frozen --no-editable


# ── Stage 2: runtime ──────────────────────────────────────────────────────────
FROM python:{{ cookiecutter.python_version }}-slim AS runtime

WORKDIR /app

RUN apt-get update && apt-get upgrade -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --system {{ cookiecutter.package_name }} \
    && useradd --system --gid {{ cookiecutter.package_name }} --no-create-home {{ cookiecutter.package_name }}

COPY --from=python-deps /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

RUN mkdir -p /app/staticfiles /app/media /shared \
    && chown -R {{ cookiecutter.package_name }}:{{ cookiecutter.package_name }} /app/staticfiles /app/media /shared

COPY docker/app/conf/uwsgi.ini /app/uwsgi.ini
COPY docker/app/conf/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENV DJANGO_SETTINGS_MODULE={{ cookiecutter.package_name }}.config.settings \
    STATIC_ROOT=/app/staticfiles \
    MEDIA_ROOT=/app/media

USER {{ cookiecutter.package_name }}

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["web"]
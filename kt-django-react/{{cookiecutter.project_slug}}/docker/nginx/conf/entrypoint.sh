#!/bin/sh
set -e

PREFIXES_FILE=/shared/url_prefixes.json
ROUTES_CONF=/etc/nginx/conf.d/backend_routes.conf
APP_UPSTREAM="${APP_UPSTREAM:-{{ cookiecutter.project_slug }}-app:8000}"

echo "Waiting for URL prefixes file..."
until [ -f "$PREFIXES_FILE" ]; do
    sleep 1
done

echo "Generating backend route configuration (upstream: $APP_UPSTREAM)..."
> "$ROUTES_CONF"
jq -r '.[]' "$PREFIXES_FILE" | while IFS= read -r prefix; do
    printf 'location /%s/ {\n    include uwsgi_params;\n    uwsgi_pass %s;\n}\n\n' "$prefix" "$APP_UPSTREAM"
done >> "$ROUTES_CONF"

echo "Starting nginx..."
exec nginx -g 'daemon off;'
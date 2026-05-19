# ── Stage 1: build the React frontend ────────────────────────────────────────
FROM node:22-alpine AS frontend-builder

WORKDIR /app

COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build


# ── Stage 2: runtime ──────────────────────────────────────────────────────────
FROM nginx:alpine AS runtime

RUN apk upgrade --no-cache && apk add --no-cache jq

COPY --from=frontend-builder /app/dist/ /var/www/html/
COPY docker/nginx/conf/nginx.conf /etc/nginx/nginx.conf
COPY docker/nginx/conf/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
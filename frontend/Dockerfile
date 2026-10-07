FROM ghcr.io/cirruslabs/flutter:3.29.3 AS build

WORKDIR /app
COPY pubspec.yaml ./
RUN flutter pub get

COPY . .
ARG API_BASE_URL=
RUN flutter build web --release --dart-define=API_BASE_URL=${API_BASE_URL}

FROM nginxinc/nginx-unprivileged:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/build/web /usr/share/nginx/html

EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD wget --spider --quiet http://127.0.0.1:8080/ || exit 1

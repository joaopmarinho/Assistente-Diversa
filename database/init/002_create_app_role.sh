#!/bin/bash
set -euo pipefail

psql \
    --username "$POSTGRES_USER" \
    --dbname "$POSTGRES_DB" \
    --set=ON_ERROR_STOP=1 \
    --set=app_password="$POSTGRES_APP_PASSWORD" <<'SQL'
SELECT format('CREATE ROLE assistente_app LOGIN PASSWORD %L', :'app_password') \gexec
GRANT CONNECT ON DATABASE assistente_diversa TO assistente_app;
GRANT USAGE ON SCHEMA public TO assistente_app;
GRANT SELECT ON TABLE articles TO assistente_app;
SQL

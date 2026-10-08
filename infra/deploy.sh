#!/usr/bin/env bash
# Uso: ALERT_EMAIL=voce@exemplo.com GROQ_KEY=... ./deploy.sh
set -euo pipefail

: "${ALERT_EMAIL:?Defina ALERT_EMAIL}"
STACK="${STACK_NAME:-assistente-diversa}"
cd "$(dirname "$0")"

sam build --template-file template.yaml
sam deploy \
  --stack-name "$STACK" \
  --resolve-s3 --resolve-image-repos \
  --capabilities CAPABILITY_IAM \
  --no-confirm-changeset --no-fail-on-empty-changeset \
  --parameter-overrides "GroqKey=${GROQ_KEY:-}" "AlertEmail=${ALERT_EMAIL}"

saida() {
  aws cloudformation describe-stacks --stack-name "$STACK" \
    --query "Stacks[0].Outputs[?OutputKey=='$1'].OutputValue" --output text
}

(cd ../frontend && npm ci && npm run build)
aws s3 sync ../frontend/dist "s3://$(saida BucketName)" --delete
aws cloudfront create-invalidation --distribution-id "$(saida DistributionId)" --paths "/*" >/dev/null

echo "Site: $(saida SiteUrl)"

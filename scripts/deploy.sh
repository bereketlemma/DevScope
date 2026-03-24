#!/usr/bin/env bash
# Deploy all DevScope services to Cloud Run
set -euo pipefail

source .env 2>/dev/null || true
PROJECT_ID="${GCP_PROJECT_ID:?Set GCP_PROJECT_ID}"
REGION="${GCP_REGION:-us-central1}"
AR_REPO="${REGION}-docker.pkg.dev/${PROJECT_ID}/devscope"
TAG="${1:-latest}"

echo "=== Deploying DevScope (tag: $TAG) ==="

# Configure Docker auth
gcloud auth configure-docker "${REGION}-docker.pkg.dev" --quiet

# Build and push ingestion
echo "--- Ingestion Service ---"
docker build -t "${AR_REPO}/ingestion:${TAG}" ./ingestion
docker push "${AR_REPO}/ingestion:${TAG}"
gcloud run deploy devscope-ingestion \
  --image="${AR_REPO}/ingestion:${TAG}" \
  --region="$REGION" \
  --set-env-vars="GCP_PROJECT_ID=${PROJECT_ID},PUBSUB_TOPIC_EVENTS=github-events" \
  --allow-unauthenticated --quiet

# Build and push API
echo "--- API Service ---"
docker build -t "${AR_REPO}/api:${TAG}" ./api
docker push "${AR_REPO}/api:${TAG}"
gcloud run deploy devscope-api \
  --image="${AR_REPO}/api:${TAG}" \
  --region="$REGION" \
  --set-env-vars="GCP_PROJECT_ID=${PROJECT_ID},BQ_DATASET=devscope_prod" \
  --allow-unauthenticated --quiet

echo ""
echo "=== Deployment complete ==="
gcloud run services list --region="$REGION" --filter="metadata.name~devscope"

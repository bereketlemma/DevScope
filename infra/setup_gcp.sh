#!/usr/bin/env bash
# DevScope — GCP Resource Setup
# Run once to provision all required GCP resources.
#
# Prerequisites:
#   - gcloud CLI authenticated (gcloud auth login)
#   - Billing enabled on the project
#
# Usage: ./infra/setup_gcp.sh

set -euo pipefail

# Load config
source .env 2>/dev/null || true
PROJECT_ID="${GCP_PROJECT_ID:?Set GCP_PROJECT_ID in .env}"
REGION="${GCP_REGION:-us-central1}"
BQ_DATASET="${BQ_DATASET:-devscope_dev}"
BQ_LOCATION="${BQ_LOCATION:-US}"
PUBSUB_TOPIC="${PUBSUB_TOPIC_EVENTS:-github-events}"
PUBSUB_DLQ="${PUBSUB_TOPIC_DLQ:-github-events-dlq}"
PUBSUB_SUB="${PUBSUB_SUBSCRIPTION:-github-events-sub}"

echo "=== DevScope GCP Setup ==="
echo "Project: $PROJECT_ID"
echo "Region:  $REGION"
echo ""

# 1. Set project
gcloud config set project "$PROJECT_ID"

# 2. Enable APIs
echo "--- Enabling APIs ---"
gcloud services enable \
  bigquery.googleapis.com \
  pubsub.googleapis.com \
  dataflow.googleapis.com \
  run.googleapis.com \
  aiplatform.googleapis.com \
  artifactregistry.googleapis.com \
  secretmanager.googleapis.com \
  cloudbuild.googleapis.com \
  storage.googleapis.com

# 3. Create BigQuery dataset
echo "--- Creating BigQuery dataset: $BQ_DATASET ---"
bq --location="$BQ_LOCATION" mk --dataset \
  --description "DevScope analytics data" \
  "${PROJECT_ID}:${BQ_DATASET}" 2>/dev/null || echo "Dataset already exists"

# 4. Create BigQuery tables
echo "--- Creating BigQuery tables ---"
bq mk --table \
  --time_partitioning_field created_date \
  --clustering_fields repo_id \
  "${PROJECT_ID}:${BQ_DATASET}.pull_requests" \
  infra/schemas/pull_requests.json 2>/dev/null || echo "pull_requests table exists"

bq mk --table \
  --time_partitioning_field committed_date \
  --clustering_fields repo_id \
  "${PROJECT_ID}:${BQ_DATASET}.commits" \
  infra/schemas/commits.json 2>/dev/null || echo "commits table exists"

bq mk --table \
  --clustering_fields repo_id \
  "${PROJECT_ID}:${BQ_DATASET}.reviews" \
  infra/schemas/reviews.json 2>/dev/null || echo "reviews table exists"

bq mk --table \
  --time_partitioning_field metric_date \
  --clustering_fields repo_id \
  "${PROJECT_ID}:${BQ_DATASET}.daily_metrics" \
  infra/schemas/daily_metrics.json 2>/dev/null || echo "daily_metrics table exists"

# 5. Create Pub/Sub topics and subscriptions
echo "--- Creating Pub/Sub resources ---"
gcloud pubsub topics create "$PUBSUB_TOPIC" 2>/dev/null || echo "Topic exists"
gcloud pubsub topics create "$PUBSUB_DLQ" 2>/dev/null || echo "DLQ topic exists"
gcloud pubsub subscriptions create "$PUBSUB_SUB" \
  --topic="$PUBSUB_TOPIC" \
  --ack-deadline=60 \
  --dead-letter-topic="$PUBSUB_DLQ" \
  --max-delivery-attempts=5 \
  2>/dev/null || echo "Subscription exists"

# 6. Create GCS bucket for Dataflow temp + ML models
echo "--- Creating GCS buckets ---"
gsutil mb -l "$REGION" "gs://${PROJECT_ID}-dataflow-temp" 2>/dev/null || echo "Dataflow bucket exists"
gsutil mb -l "$REGION" "gs://${PROJECT_ID}-devscope-models" 2>/dev/null || echo "Models bucket exists"

# 7. Create Artifact Registry repo
echo "--- Creating Artifact Registry ---"
gcloud artifacts repositories create devscope \
  --repository-format=docker \
  --location="$REGION" \
  --description="DevScope container images" \
  2>/dev/null || echo "Artifact Registry exists"

# 8. Create service account
echo "--- Creating service account ---"
SA_NAME="devscope-runner"
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

gcloud iam service-accounts create "$SA_NAME" \
  --display-name="DevScope Service Account" \
  2>/dev/null || echo "Service account exists"

# Grant roles
for ROLE in \
  roles/bigquery.admin \
  roles/pubsub.publisher \
  roles/pubsub.subscriber \
  roles/run.invoker \
  roles/dataflow.worker \
  roles/aiplatform.user \
  roles/storage.admin \
  roles/secretmanager.secretAccessor; do
  gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:$SA_EMAIL" \
    --role="$ROLE" \
    --quiet
done

# Download key
echo "--- Downloading service account key ---"
gcloud iam service-accounts keys create service-account.json \
  --iam-account="$SA_EMAIL" 2>/dev/null || echo "Key exists"

# 9. Set billing alerts
echo "--- Setting billing alerts ---"
echo "  ⚠ Set billing alerts manually at:"
echo "  https://console.cloud.google.com/billing/${PROJECT_ID}/budgets"
echo "  Recommended: \$50, \$100, \$200, \$300"

echo ""
echo "=== Setup complete! ==="
echo "Next steps:"
echo "  1. cp .env.example .env && edit .env with your values"
echo "  2. make setup"
echo "  3. make dev"

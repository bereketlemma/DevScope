"""Configuration for the API service."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    gcp_project_id: str = os.getenv("GCP_PROJECT_ID", "")
    bq_dataset: str = os.getenv("BQ_DATASET", "devscope_dev")
    bq_location: str = os.getenv("BQ_LOCATION", "US")
    frontend_url: str = os.getenv("FRONTEND_URL", "*")
    environment: str = os.getenv("ENVIRONMENT", "development")
    port: int = int(os.getenv("API_PORT", "8000"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    vertex_endpoint_id: str = os.getenv("VERTEX_ENDPOINT_ID", "")
    vertex_model_id: str = os.getenv("VERTEX_MODEL_ID", "")
    gcp_region: str = os.getenv("GCP_REGION", "us-central1")


config = Config()

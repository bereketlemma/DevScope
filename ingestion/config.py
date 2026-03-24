"""Configuration for the ingestion service."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    """Ingestion service configuration loaded from environment."""

    gcp_project_id: str = os.getenv("GCP_PROJECT_ID", "")
    pubsub_topic: str = os.getenv("PUBSUB_TOPIC_EVENTS", "github-events")
    pubsub_dlq_topic: str = os.getenv("PUBSUB_TOPIC_DLQ", "github-events-dlq")
    github_token: str = os.getenv("GITHUB_TOKEN", "")
    github_webhook_secret: str = os.getenv("GITHUB_WEBHOOK_SECRET", "")
    default_lookback_days: int = int(os.getenv("DEFAULT_LOOKBACK_DAYS", "90"))
    environment: str = os.getenv("ENVIRONMENT", "development")
    port: int = int(os.getenv("INGESTION_PORT", "8001"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    def validate(self) -> None:
        """Raise ValueError if required fields are missing."""
        if not self.gcp_project_id:
            raise ValueError("GCP_PROJECT_ID is required")
        if not self.github_token:
            raise ValueError("GITHUB_TOKEN is required")


config = Config()

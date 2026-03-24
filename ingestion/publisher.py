"""Publishes GitHub events to Cloud Pub/Sub for downstream processing."""

from __future__ import annotations

import json
import logging
from typing import Any

from google.cloud import pubsub_v1
from google.api_core import exceptions as gcp_exceptions

from config import config

logger = logging.getLogger(__name__)


class EventPublisher:
    """Publishes structured GitHub events to Pub/Sub topics."""

    def __init__(self) -> None:
        self._publisher = pubsub_v1.PublisherClient()
        self._topic_path = self._publisher.topic_path(
            config.gcp_project_id, config.pubsub_topic
        )
        self._dlq_topic_path = self._publisher.topic_path(
            config.gcp_project_id, config.pubsub_dlq_topic
        )

    def _serialize(self, event: dict[str, Any]) -> bytes:
        """Serialize event to JSON bytes."""
        return json.dumps(event, default=str).encode("utf-8")

    async def publish_event(
        self,
        event_type: str,
        repo_id: str,
        payload: dict[str, Any],
    ) -> str:
        """
        Publish a single event to the github-events topic.

        Args:
            event_type: One of 'pull_request', 'commit', 'review'
            repo_id: GitHub repo full name (owner/repo)
            payload: The event data

        Returns:
            Published message ID
        """
        message = {
            "event_type": event_type,
            "repo_id": repo_id,
            "payload": payload,
        }

        try:
            future = self._publisher.publish(
                self._topic_path,
                data=self._serialize(message),
                event_type=event_type,
                repo_id=repo_id,
            )
            message_id = future.result(timeout=30)
            logger.debug("Published %s event: %s", event_type, message_id)
            return message_id

        except gcp_exceptions.GoogleAPIError as e:
            logger.error("Failed to publish %s event: %s", event_type, e)
            # Attempt DLQ
            self._publish_to_dlq(message, str(e))
            raise

    def _publish_to_dlq(self, message: dict[str, Any], error: str) -> None:
        """Send failed messages to the dead-letter queue topic."""
        try:
            dlq_message = {"original_message": message, "error": error}
            self._publisher.publish(
                self._dlq_topic_path,
                data=self._serialize(dlq_message),
            )
            logger.info("Message sent to DLQ")
        except Exception:
            logger.exception("Failed to publish to DLQ")

    async def publish_batch(
        self,
        event_type: str,
        repo_id: str,
        payloads: list[dict[str, Any]],
    ) -> list[str]:
        """Publish a batch of events. Returns list of message IDs."""
        message_ids = []
        for payload in payloads:
            mid = await self.publish_event(event_type, repo_id, payload)
            message_ids.append(mid)
        return message_ids

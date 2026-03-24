"""
DevScope Stream Processing Pipeline

Reads GitHub events from Cloud Pub/Sub, transforms them, and writes
to BigQuery tables partitioned by date and clustered by repo_id.

Usage:
  # Local (DirectRunner)
  python main.py --runner DirectRunner

  # Cloud Dataflow
  python main.py \
    --runner DataflowRunner \
    --project YOUR_PROJECT \
    --region us-central1 \
    --temp_location gs://YOUR_BUCKET/tmp \
    --streaming
"""

from __future__ import annotations

import argparse
import logging
import os

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions

from schemas import PULL_REQUESTS_SCHEMA, COMMITS_SCHEMA, REVIEWS_SCHEMA
from transforms import (
    ParsePubSubMessage,
    RoutByEventType,
    TransformPullRequest,
    TransformCommit,
    TransformReview,
)

logger = logging.getLogger(__name__)

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "")
DATASET = os.getenv("BQ_DATASET", "devscope_dev")
PUBSUB_SUBSCRIPTION = os.getenv("PUBSUB_SUBSCRIPTION", "github-events-sub")


def build_table_ref(table_name: str) -> str:
    """Build a BigQuery table reference string."""
    return f"{PROJECT_ID}:{DATASET}.{table_name}"


def run(argv: list[str] | None = None) -> None:
    """Build and run the streaming pipeline."""
    parser = argparse.ArgumentParser()
    known_args, pipeline_args = parser.parse_known_args(argv)

    options = PipelineOptions(pipeline_args)
    options.view_as(StandardOptions).streaming = True

    subscription = f"projects/{PROJECT_ID}/subscriptions/{PUBSUB_SUBSCRIPTION}"

    with beam.Pipeline(options=options) as p:
        # 1. Read from Pub/Sub
        raw_messages = (
            p
            | "ReadPubSub" >> beam.io.ReadFromPubSub(subscription=subscription)
            | "ParseMessages" >> beam.ParDo(ParsePubSubMessage())
        )

        # 2. Route events by type
        routed = raw_messages | "RouteByType" >> beam.ParDo(
            RoutByEventType()
        ).with_outputs("pull_requests", "commits", "reviews")

        # 3. Transform and write pull requests
        (
            routed.pull_requests
            | "TransformPRs" >> beam.ParDo(TransformPullRequest())
            | "WritePRs" >> beam.io.WriteToBigQuery(
                table=build_table_ref("pull_requests"),
                schema={"fields": PULL_REQUESTS_SCHEMA},
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
            )
        )

        # 4. Transform and write commits
        (
            routed.commits
            | "TransformCommits" >> beam.ParDo(TransformCommit())
            | "WriteCommits" >> beam.io.WriteToBigQuery(
                table=build_table_ref("commits"),
                schema={"fields": COMMITS_SCHEMA},
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
            )
        )

        # 5. Transform and write reviews
        (
            routed.reviews
            | "TransformReviews" >> beam.ParDo(TransformReview())
            | "WriteReviews" >> beam.io.WriteToBigQuery(
                table=build_table_ref("reviews"),
                schema={"fields": REVIEWS_SCHEMA},
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
            )
        )

    logger.info("Pipeline complete")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run()

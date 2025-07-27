"""
Kafka producer utilities for the auth service.

This module defines a simple wrapper around kafka-python to publish
domain events.  Events are encoded as dictionaries and serialised
to JSON before sending to Kafka.
"""

import json
import os
from typing import Dict

from kafka import KafkaProducer


_producer = None


def get_producer() -> KafkaProducer:
    """Lazy-initialise and return a Kafka producer."""
    global _producer
    if _producer is None:
        bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
        _producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            key_serializer=lambda k: k.encode("utf-8") if k else None,
        )
    return _producer


def publish_event(topic: str, message: Dict, key: str | None = None) -> None:
    """Publish a JSON-serialisable event on the given Kafka topic."""
    producer = get_producer()
    producer.send(topic, value=message, key=key)
    # Fire-and-forget; in a production system you may wish to block on flush
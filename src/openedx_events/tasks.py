"""
Celery tasks for sending Open edX events asynchronously.
"""

import base64
from logging import getLogger

from celery import shared_task

log = getLogger(__name__)


@shared_task(name="openedx_events.tasks.send_async_event")
def send_async_event(event_type: str, metadata_json: str, event_data_b64: str) -> None:
    """
    Re-send an event from a Celery worker.

    Event data is serialized using the Avro serializer (because event payloads
    are typically attrs classes that are not JSON-serializable) and base64-encoded
    so that it can be passed as a JSON-safe argument to Celery. Metadata is
    passed as a JSON string.

    Arguments:
        event_type (str): The event type of the signal to re-send.
        metadata_json (str): JSON-serialized EventsMetadata.
        event_data_b64 (str): Base64-encoded Avro-serialized event data.
    """
    # Imported here to avoid a circular import at module load time.
    from .data import EventsMetadata  # pylint: disable=import-outside-toplevel
    from .event_bus.avro.deserializer import deserialize_bytes_to_event_data  # pylint: disable=import-outside-toplevel
    from .tooling import OpenEdxPublicSignal  # pylint: disable=import-outside-toplevel,cyclic-import

    signal = OpenEdxPublicSignal.get_signal_by_type(event_type)
    metadata = EventsMetadata.from_json(metadata_json)
    event_data = deserialize_bytes_to_event_data(
        base64.b64decode(event_data_b64), signal
    )
    signal._send_event_with_metadata(  # pylint: disable=protected-access
        metadata=metadata,
        **event_data,
    )

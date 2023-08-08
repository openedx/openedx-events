""" Tests for openedx_events.data module."""
from datetime import datetime, timezone
from uuid import UUID

from django.test import TestCase

from openedx_events.data import EventsMetadata


class TestEventsMetadata(TestCase):
    """
    Tests for the EventsMetadata class.
    """
    def setUp(self) -> None:
        self.now = datetime.now(timezone.utc)
        self.metadata = EventsMetadata(
            event_type='test_type',
            time=self.now,
            source='test_source',
            sourcehost='test_source_host',
            sourcelib=(1, 2, 3),
            id=UUID('c45efb10-3556-11ee-9f19-7e694b1e500b')
        )

    def test_events_metadata_to_and_from_json(self):
        as_json = self.metadata.as_json()
        from_json = EventsMetadata.from_json(as_json)
        self.assertEqual(self.metadata, from_json)

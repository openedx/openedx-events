""" Tests for openedx_events.data module."""
from datetime import datetime, timezone
from uuid import UUID

import ddt
from django.test import TestCase
from django.test.utils import override_settings

from openedx_events.data import EventsMetadata


@ddt.ddt
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
        as_json = self.metadata.to_json()
        from_json = EventsMetadata.from_json(as_json)
        self.assertEqual(self.metadata, from_json)

    @ddt.data(
        ('settings_variant', None, 'openedx/settings_variant/web'),
        (None, 'my_service', 'openedx/my_service/web'),
        (None, None, 'openedx//web'),
        ('settings_variant', 'my_service', 'openedx/my_service/web')
    )
    @ddt.unpack
    def test_events_metadata_source(self, settings_variant, event_bus_service_name, expected_source):
        with override_settings(
                SERVICE_VARIANT=settings_variant,
                EVENT_BUS_APP_NAME=event_bus_service_name,
        ):
            metadata = EventsMetadata(
                event_type='test_type'
            )
            self.assertEqual(metadata.source, expected_source)

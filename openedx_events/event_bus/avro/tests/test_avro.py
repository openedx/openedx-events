"""Test interplay of the various Avro helper classes"""
from unittest import TestCase

from openedx_events.event_bus.avro.tests.test_utilities import (
    EventData,
    NestedAttrsWithDefaults,
    SimpleAttrsWithDefaults,
    SubTestData0,
    SubTestData1,
    create_simple_signal,
    deserialize_bytes_to_event_data,
    serialize_event_data_to_bytes,
)


class TestAvro(TestCase):
    """Tests for end-to-end serialization and deserialization of events"""

    def test_full_serialize_deserialize(self):
        SIGNAL = create_simple_signal({"test_data": EventData})
        event_data = {"test_data": EventData(
            "foo",
            "bar.course",
            SubTestData0("a.sub.name", "a.nother.course"),
            SubTestData1("b.uber.sub.name", "b.uber.another.course"),
        )}
        serialized = serialize_event_data_to_bytes(event_data, SIGNAL)
        deserialized = deserialize_bytes_to_event_data(serialized, SIGNAL)
        self.assertIsInstance(deserialized["test_data"], EventData)
        self.assertEqual(deserialized, event_data)
        # ensure signal can actually send deserialized event data
        SIGNAL.send_event(**deserialized)

    def test_full_serialize_deserialize_with_optional_fields(self):
        SIGNAL = create_simple_signal({"test_data": NestedAttrsWithDefaults})
        event_data = {"test_data": NestedAttrsWithDefaults(field_0=SimpleAttrsWithDefaults())}
        serialized = serialize_event_data_to_bytes(event_data, SIGNAL)
        deserialized = deserialize_bytes_to_event_data(serialized, SIGNAL)
        self.assertIsInstance(deserialized["test_data"], NestedAttrsWithDefaults)
        self.assertEqual(deserialized, event_data)
        # ensure signal can actually send deserialized event data
        SIGNAL.send_event(**deserialized)

"""Test interplay of the various Avro helper classes"""
import io
from unittest import TestCase

import fastavro

from openedx_events.event_bus.avro.deserializer import AvroSignalDeserializer
from openedx_events.event_bus.avro.serializer import AvroSignalSerializer
from openedx_events.event_bus.avro.tests.test_utilities import (
    EventData,
    NestedAttrsWithDefaults,
    SimpleAttrsWithDefaults,
    SubTestData0,
    SubTestData1,
    create_simple_signal,
)


def serialize_and_deserialize_event_data(signal, event_data):
    """Utility method convert events to Avro records and back """
    serializer = AvroSignalSerializer(signal)
    deserializer = AvroSignalDeserializer(signal)
    schema_dict = serializer.schema
    out = io.BytesIO()
    data_dict = serializer.to_dict(event_data)
    fastavro.schemaless_writer(out, schema_dict, data_dict)
    out.seek(0)
    as_bytes = out.read()
    deserializer_schema_dict = deserializer.schema
    data_file = io.BytesIO(as_bytes)
    as_dict = fastavro.schemaless_reader(data_file, deserializer_schema_dict)
    return deserializer.from_dict(as_dict)


class TestAvro(TestCase):
    """Tests for end-to-end serialization and deserialization of events"""

    def test_full_serialize_deserialize(self):
        SIGNAL = create_simple_signal({"test_data": EventData})
        event_data = EventData(
            "foo",
            "bar.course",
            SubTestData0("a.sub.name", "a.nother.course"),
            SubTestData1("b.uber.sub.name", "b.uber.another.course"),
        )
        original_data = serialize_and_deserialize_event_data(SIGNAL, {"test_data": event_data})['test_data']
        self.assertIsInstance(original_data, EventData)
        self.assertEqual(original_data.sub_name, 'foo')
        self.assertEqual(original_data.course_id, 'bar.course')
        self.assertIsInstance(original_data.sub_test_0, SubTestData0)
        self.assertEqual(original_data.sub_test_0.sub_name, 'a.sub.name')
        self.assertEqual(original_data.sub_test_0.course_id, 'a.nother.course')
        self.assertIsInstance(original_data.sub_test_1, SubTestData1)
        self.assertEqual(original_data.sub_test_1.sub_name, 'b.uber.sub.name')
        self.assertEqual(original_data.sub_test_1.course_id, 'b.uber.another.course')
        # ensure signal can actually send deserialized event data
        SIGNAL.send_event(test_data=original_data)

    def test_full_serialize_deserialize_with_optional_fields(self):
        SIGNAL = create_simple_signal({"test_data": NestedAttrsWithDefaults})
        event_data = NestedAttrsWithDefaults(field_0=SimpleAttrsWithDefaults())
        original_data = serialize_and_deserialize_event_data(SIGNAL, {"test_data": event_data})['test_data']
        self.assertIsInstance(original_data, NestedAttrsWithDefaults)
        original_sub_data = original_data.field_0
        self.assertIsInstance(original_sub_data, SimpleAttrsWithDefaults)
        self.assertEqual(original_sub_data.boolean_field, None)
        self.assertEqual(original_sub_data.int_field, None)
        self.assertEqual(original_sub_data.bytes_field, None)
        self.assertEqual(original_sub_data.float_field, None)
        self.assertEqual(original_sub_data.attrs_field, None)
        # ensure signal can actually send deserialized event data
        SIGNAL.send_event(test_data=original_data)

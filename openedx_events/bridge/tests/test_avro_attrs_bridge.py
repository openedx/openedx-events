"""
Tests for AvroAttrsBridge.
"""
from datetime import datetime
from unittest import TestCase

from opaque_keys.edx.keys import CourseKey

from openedx_events.bridge.avro_attrs_bridge import AvroAttrsBridge
from openedx_events.bridge.tests.test_utilities import (
    NestedAttrsWithDefaults,
    NonAttrs,
    SimpleAttrs,
    SimpleAttrsWithDefaults,
    SimpleBridgeExtension,
    SubTestData0,
    SubTestData1,
    TestData,
    create_simple_signal,
    deserialize_bytes_to_event_data,
    serialize_event_data_to_bytes,
)


class TestAvroAttrsBridge(TestCase):
    """
    Test AvroAttrsBridge functionality
    """

    def test_simple_schema_generation(self):
        SIGNAL = create_simple_signal({"event_data": SimpleAttrs})

        bridge = AvroAttrsBridge(SIGNAL)
        expected_dict = {
            "type": "record",
            "name": "CloudEvent",
            "doc": "Avro Event Format for CloudEvents created with openedx_events/avro_attrs_bridge",
            "fields": [
                {"name": "event_data", "type":
                    {"name": "SimpleAttrs", "type": "record", "fields": [
                        {"name": "boolean_field", "type": "boolean"},
                        {"name": "int_field", "type": "long"},
                        {"name": "float_field", "type": "double"},
                        {"name": "bytes_field", "type": "bytes"},
                        {"name": "string_field", "type": "string"},
                    ]
                     }
                 }
            ],
        }

        self.assertDictEqual(bridge.schema_dict, expected_dict)

    def test_nested_attrs_object_serialization(self):
        SIGNAL = create_simple_signal({"test_data": TestData})
        bridge = AvroAttrsBridge(SIGNAL)

        expected_dict = {
            "type": "record",
            "name": "CloudEvent",
            "doc": "Avro Event Format for CloudEvents created with openedx_events/avro_attrs_bridge",
            "fields": [
                {"name": "test_data", "type":
                    {"name": "TestData", "type": "record", "fields": [
                        {"name": "sub_name", "type": "string"},
                        {"name": "course_id", "type": "string"},
                        {"name": "sub_test_0", "type": {
                            "name": "SubTestData0",
                            "type": "record",
                            "fields": [
                                {"name": "sub_name", "type": "string"},
                                {"name": "course_id", "type": "string"},
                            ]
                        }},
                        {"name": "sub_test_1", "type": {
                            "name": "SubTestData1",
                            "type": "record",
                            "fields": [
                                {"name": "sub_name", "type": "string"},
                                {"name": "course_id", "type": "string"},
                            ]
                        }},
                    ]}
                 },
            ],
        }

        self.assertDictEqual(bridge.schema_dict, expected_dict)

    def test_multiple_top_level_fields(self):
        SIGNAL = create_simple_signal({
            "top_level_key_0": SubTestData0,
            "top_level_key_1": SubTestData1,
        })
        bridge = AvroAttrsBridge(SIGNAL)

        expected_dict = {
            "type": "record",
            "name": "CloudEvent",
            "doc": "Avro Event Format for CloudEvents created with openedx_events/avro_attrs_bridge",
            "fields": [
                {"name": "top_level_key_0", "type":
                    {
                        "name": "SubTestData0",
                        "type": "record",
                        "fields": [
                            {"name": "sub_name", "type": "string"},
                            {"name": "course_id", "type": "string"},
                        ]
                    }
                 },
                {"name": "top_level_key_1", "type":
                    {
                        "name": "SubTestData1",
                        "type": "record",
                        "fields": [
                            {"name": "sub_name", "type": "string"},
                            {"name": "course_id", "type": "string"},
                        ]
                    }
                 },
            ],
        }
        self.assertDictEqual(bridge.schema_dict, expected_dict)

    def test_convert_event_data_to_dict(self):
        """
        Tests that an event with complex attrs objects can be converted to dict and back
        """

        SIGNAL = create_simple_signal({"test_data": TestData})
        bridge = AvroAttrsBridge(SIGNAL)
        # A test record that we can try to serialize to avro.
        test_data = TestData(
            "foo",
            "bar.course",
            SubTestData0("a.sub.name", "a.nother.course"),
            SubTestData1("b.uber.sub.name", "b.uber.another.course"),
        )

        data_dict = bridge.to_dict({"test_data": test_data})
        expected_dict = {
            "test_data": {
                "course_id": "bar.course",
                "sub_name": "foo",
                "sub_test_0": {"course_id": "a.nother.course", "sub_name": "a.sub.name"},
                "sub_test_1": {
                    "course_id": "b.uber.another.course",
                    "sub_name": "b.uber.sub.name",
                },
            }
        }
        self.assertDictEqual(data_dict, expected_dict)

    def test_convert_dict_to_event_data(self):
        initial_dict = {
            "test_data": {
                "course_id": "bar.course",
                "sub_name": "foo",
                "sub_test_0": {"course_id": "a.nother.course", "sub_name": "a.sub.name"},
                "sub_test_1": {
                    "course_id": "b.uber.another.course",
                    "sub_name": "b.uber.sub.name",
                },
            }
        }

        SIGNAL = create_simple_signal({"test_data": TestData})
        bridge = AvroAttrsBridge(SIGNAL)
        event_data = bridge.from_dict(initial_dict)

        test_data = event_data["test_data"]
        self.assertIsInstance(test_data, TestData)
        self.assertEqual(test_data.course_id, "bar.course")
        self.assertEqual(test_data.sub_name, "foo")

        sub_0 = test_data.sub_test_0
        self.assertIsInstance(sub_0, SubTestData0)
        self.assertEqual(sub_0.course_id, "a.nother.course")
        self.assertEqual(sub_0.sub_name, "a.sub.name")

        sub_1 = test_data.sub_test_1
        self.assertIsInstance(sub_1, SubTestData1)
        self.assertEqual(sub_1.course_id, "b.uber.another.course")
        self.assertEqual(sub_1.sub_name, "b.uber.sub.name")

    def test_full_serialize_and_deserialize(self):
        SIGNAL = create_simple_signal({"test_data": TestData})
        bridge = AvroAttrsBridge(SIGNAL)
        test_data = {"test_data": TestData(
            "foo",
            "bar.course",
            SubTestData0("a.sub.name", "a.nother.course"),
            SubTestData1("b.uber.sub.name", "b.uber.another.course"),
        )}

        as_bytes = serialize_event_data_to_bytes(bridge, test_data)
        deserialized = deserialize_bytes_to_event_data(bridge, as_bytes)
        self.assertEqual(test_data, deserialized)
        # check we can emit the deserialized event with the original signal
        SIGNAL.send_event(**deserialized)

    def test_default_datetime_extension_serialization(self):
        SIGNAL = create_simple_signal({"birthday": datetime})
        bridge = AvroAttrsBridge(SIGNAL)
        birthday = datetime(year=1989, month=9, day=6)
        test_data = {"birthday": birthday}
        data_dict = bridge.to_dict(test_data)
        assert data_dict == {"birthday": birthday.isoformat()}

    def test_default_datetime_extension_deserialization(self):
        SIGNAL = create_simple_signal({"birthday": datetime})
        bridge = AvroAttrsBridge(SIGNAL)
        birthday = datetime(year=1989, month=9, day=6)
        as_dict = {"birthday": birthday.isoformat()}
        event_data = bridge.from_dict(as_dict)
        birthday_deserialized = event_data["birthday"]
        self.assertIsInstance(birthday_deserialized, datetime)
        self.assertEqual(birthday_deserialized.year, 1989)
        self.assertEqual(birthday_deserialized.month, 9)
        self.assertEqual(birthday_deserialized.day, 6)

    def test_default_coursekey_extension_serialization(self):
        SIGNAL = create_simple_signal({"course": CourseKey})
        bridge = AvroAttrsBridge(SIGNAL)
        course_key = CourseKey.from_string("course-v1:edX+DemoX.1+2014")
        test_data = {"course": course_key}
        data_dict = bridge.to_dict(test_data)
        assert data_dict == {"course": str(course_key)}

    def test_default_coursekey_extension_deserialization(self):
        SIGNAL = create_simple_signal({"course": CourseKey})
        bridge = AvroAttrsBridge(SIGNAL)
        course_key = CourseKey.from_string("course-v1:edX+DemoX.1+2014")
        as_dict = {"course": str(course_key)}
        event_data = bridge.from_dict(as_dict)
        course_deserialized = event_data["course"]
        self.assertIsInstance(course_deserialized, CourseKey)
        self.assertEqual(course_deserialized, course_key)

    def test_custom_serializer(self):
        SIGNAL = create_simple_signal({"test_data": NonAttrs})
        bridge = AvroAttrsBridge(SIGNAL, extensions={SimpleBridgeExtension.cls: SimpleBridgeExtension()})
        test_data = {
            "test_data": NonAttrs("a.val", "a.nother.val")
        }
        as_bytes = serialize_event_data_to_bytes(bridge, test_data)
        self.assertEqual(test_data, deserialize_bytes_to_event_data(bridge, as_bytes))

    def test_throw_exception_on_unextended_custom_type(self):
        class UnextendedClass:
            pass

        SIGNAL = create_simple_signal({"unextended_class": UnextendedClass})
        with self.assertRaises(TypeError):
            AvroAttrsBridge(SIGNAL)

    def test_dict_to_event_data_fails_if_missing_fields(self):
        # missing "sub_name" field
        initial_dict = {
            "test_data": {
                "course_id": "bar.course",
            }
        }

        SIGNAL = create_simple_signal({"test_data": SubTestData0})
        bridge = AvroAttrsBridge(SIGNAL)
        with self.assertRaises(TypeError):
            _ = bridge.from_dict(initial_dict)

    def test_throw_exception_to_list_or_dict_types(self):
        LIST_SIGNAL = create_simple_signal({"list_input": list})
        DICT_SIGNAL = create_simple_signal({"list_input": dict})
        with self.assertRaises(Exception):
            AvroAttrsBridge(LIST_SIGNAL)

        with self.assertRaises(Exception):
            AvroAttrsBridge(DICT_SIGNAL)

    def test_optional_fields(self):
        SIGNAL = create_simple_signal({
            "data": SimpleAttrsWithDefaults
        })
        bridge = AvroAttrsBridge(SIGNAL)
        event_data = {"data": SimpleAttrsWithDefaults()}
        as_bytes = serialize_event_data_to_bytes(bridge, event_data)
        deserialized = deserialize_bytes_to_event_data(bridge, as_bytes)
        simple_attrs = deserialized["data"]
        self.assertIsNone(simple_attrs.boolean_field)
        self.assertIsNone(simple_attrs.int_field)
        self.assertIsNone(simple_attrs.float_field)
        self.assertIsNone(simple_attrs.bytes_field)
        self.assertIsNone(simple_attrs.string_field)

    def test_nested_optional_fields(self):
        SIGNAL = create_simple_signal({
            "data": NestedAttrsWithDefaults
        })
        bridge = AvroAttrsBridge(SIGNAL)
        event_data = {"data": NestedAttrsWithDefaults()}
        as_bytes = serialize_event_data_to_bytes(bridge, event_data)
        deserialized = deserialize_bytes_to_event_data(bridge, as_bytes)
        simple_attrs = deserialized["data"]
        self.assertIsNone(simple_attrs.field_0)

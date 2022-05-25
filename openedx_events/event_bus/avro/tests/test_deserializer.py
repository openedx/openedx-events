"""Tests for avro.deserializer"""
from datetime import datetime
from unittest import TestCase

from opaque_keys.edx.keys import CourseKey

from openedx_events.event_bus.avro.deserializer import AvroSignalDeserializer
from openedx_events.event_bus.avro.tests.test_utilities import (
    EventData,
    NestedAttrsWithDefaults,
    NestedNonAttrs,
    NonAttrs,
    SimpleAttrsWithDefaults,
    SpecialDeserializer,
    SubTestData0,
    SubTestData1,
    create_simple_signal,
)


class TestAvroSignalDeserializer(TestCase):
    """Test AvroSignalDeserializer"""

    def test_convert_dict_to_event_data(self):
        SIGNAL = create_simple_signal({"test_data": EventData})
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
        deserializer = AvroSignalDeserializer(SIGNAL)

        event_data = deserializer.from_dict(initial_dict)

        test_data = event_data["test_data"]
        self.assertIsInstance(test_data, EventData)
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

    def test_default_datetime_extension_deserialization(self):
        SIGNAL = create_simple_signal({"birthday": datetime})
        deserializer = AvroSignalDeserializer(SIGNAL)
        birthday = datetime(year=1989, month=9, day=6)
        as_dict = {"birthday": birthday.isoformat()}
        event_data = deserializer.from_dict(as_dict)
        birthday_deserialized = event_data["birthday"]
        self.assertIsInstance(birthday_deserialized, datetime)
        self.assertEqual(birthday_deserialized.year, 1989)
        self.assertEqual(birthday_deserialized.month, 9)
        self.assertEqual(birthday_deserialized.day, 6)

    def test_default_coursekey_extension_deserialization(self):
        SIGNAL = create_simple_signal({"course": CourseKey})
        deserializer = AvroSignalDeserializer(SIGNAL)
        course_key = CourseKey.from_string("course-v1:edX+DemoX.1+2014")
        as_dict = {"course": str(course_key)}
        event_data = deserializer.from_dict(as_dict)
        course_deserialized = event_data["course"]
        self.assertIsInstance(course_deserialized, CourseKey)
        self.assertEqual(course_deserialized, course_key)

    def test_deserialization_with_custom_serializer(self):
        SIGNAL = create_simple_signal({"test_data": NonAttrs})
        deserializer = SpecialDeserializer(SIGNAL)
        as_dict = {
            "test_data": "a.val:a.nother.val"
        }
        event_data = deserializer.from_dict(as_dict)
        non_attrs_deserialized = event_data["test_data"]
        self.assertIsInstance(non_attrs_deserialized, NonAttrs)
        self.assertEqual(non_attrs_deserialized, NonAttrs("a.val", "a.nother.val"))

    def test_deserialization_with_custom_serializer_on_nested_fields(self):
        SIGNAL = create_simple_signal({"test_data": NestedNonAttrs})
        as_dict = {"test_data": {
            "field_0": "a.val:a.nother.val"
        }}
        deserializer = SpecialDeserializer(SIGNAL)
        event_data = deserializer.from_dict(as_dict)
        deserialized_nested = event_data["test_data"]
        self.assertIsInstance(deserialized_nested, NestedNonAttrs)
        inner_deserialized_non_attrs = deserialized_nested.field_0
        self.assertIsInstance(inner_deserialized_non_attrs, NonAttrs)
        self.assertEqual(inner_deserialized_non_attrs, NonAttrs("a.val", "a.nother.val"))

    def test_deserialization_fails_if_missing_fields(self):
        # missing "sub_name" field
        initial_dict = {
            "test_data": {
                "course_id": "bar.course",
            }
        }

        SIGNAL = create_simple_signal({"test_data": SubTestData0})
        deserializer = AvroSignalDeserializer(SIGNAL)
        with self.assertRaises(TypeError):
            _ = deserializer.from_dict(initial_dict)

    def test_deserialization_of_optional_fields(self):
        SIGNAL = create_simple_signal({
            "data": SimpleAttrsWithDefaults
        })
        deserializer = AvroSignalDeserializer(SIGNAL)

        as_dict = {"data": {}}
        data_dict = deserializer.from_dict(as_dict)
        self.assertIsInstance(data_dict["data"], SimpleAttrsWithDefaults)
        self.assertIsNone(data_dict["data"].boolean_field)
        self.assertIsNone(data_dict["data"].bytes_field)
        self.assertIsNone(data_dict["data"].float_field)
        self.assertIsNone(data_dict["data"].int_field)
        self.assertIsNone(data_dict["data"].string_field)

    def test_deserialization_of_nested_optional_fields(self):
        SIGNAL = create_simple_signal({
            "data": NestedAttrsWithDefaults
        })
        deserializer = AvroSignalDeserializer(SIGNAL)
        as_dict = {"data": {"field_0": {}}}
        data_dict = deserializer.from_dict(as_dict)
        nested_field = data_dict["data"].field_0
        self.assertIsInstance(nested_field, SimpleAttrsWithDefaults)
        self.assertIsNone(nested_field.boolean_field)
        self.assertIsNone(nested_field.bytes_field)
        self.assertIsNone(nested_field.float_field)
        self.assertIsNone(nested_field.int_field)
        self.assertIsNone(nested_field.string_field)

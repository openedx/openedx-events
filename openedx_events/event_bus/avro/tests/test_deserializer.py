"""Tests for avro.deserializer"""
import json
from datetime import datetime
from typing import Dict, List
from unittest import TestCase

import ddt
from opaque_keys.edx.keys import CourseKey, UsageKey
from opaque_keys.edx.locator import LibraryLocatorV2, LibraryUsageLocatorV2

from openedx_events.event_bus.avro.deserializer import AvroSignalDeserializer, deserialize_bytes_to_event_data
from openedx_events.event_bus.avro.tests.test_utilities import (
    ComplexAttrs,
    EventData,
    NestedAttrsWithDefaults,
    NestedComplexAttrs,
    NestedNonAttrs,
    NonAttrs,
    SimpleAttrs,
    SimpleAttrsWithDefaults,
    SpecialDeserializer,
    SubTestData0,
    SubTestData1,
    create_simple_signal,
)
from openedx_events.tests.utils import FreezeSignalCacheMixin


@ddt.ddt
class TestAvroSignalDeserializerCache(TestCase, FreezeSignalCacheMixin):
    """Test AvroSignalDeserializer"""

    def setUp(self) -> None:
        super().setUp()
        self.maxDiff = None

    @ddt.data(
        (
            SimpleAttrs,
            {
                "name": "CloudEvent",
                "type": "record",
                "doc": "Avro Event Format for CloudEvents created with openedx_events/schema",
                "namespace": "simple.signal",
                "fields": [
                    {
                        "name": "data",
                        "type": {
                            "name": "SimpleAttrs",
                            "type": "record",
                            "fields": [
                                {"name": "boolean_field", "type": "boolean"},
                                {"name": "int_field", "type": "long"},
                                {"name": "float_field", "type": "double"},
                                {"name": "bytes_field", "type": "bytes"},
                                {"name": "string_field", "type": "string"},
                            ],
                        },
                    },
                ],
            },
        ),
        (
            ComplexAttrs,
            {
                "name": "CloudEvent",
                "type": "record",
                "doc": "Avro Event Format for CloudEvents created with openedx_events/schema",
                "namespace": "simple.signal",
                "fields": [
                    {
                        "name": "data",
                        "type": {
                            "name": "ComplexAttrs",
                            "type": "record",
                            "fields": [
                                {"name": "list_field", "type": {"type": "array", "items": "long"}},
                                {"name": "dict_field", "type": {"type": "map", "values": "long"}},
                            ],
                        },
                    },
                ],
            },
        ),
        (
            NestedComplexAttrs,
            {
                "name": "CloudEvent",
                "type": "record",
                "doc": "Avro Event Format for CloudEvents created with openedx_events/schema",
                "namespace": "simple.signal",
                "fields": [
                    {
                        "name": "data",
                        "type": {
                            "name": "NestedComplexAttrs",
                            "type": "record",
                            "fields": [
                                {
                                    "name": "list_of_attr_field",
                                    "type": {
                                        "type": "array",
                                        "items": {
                                            "name": "SimpleAttrs",
                                            "type": "record",
                                            "fields": [
                                                {"name": "boolean_field", "type": "boolean"},
                                                {"name": "int_field", "type": "long"},
                                                {"name": "float_field", "type": "double"},
                                                {"name": "bytes_field", "type": "bytes"},
                                                {"name": "string_field", "type": "string"},
                                            ],
                                        },
                                    },
                                },
                                {"name": "dict_of_attr_field", "type": {"type": "map", "values": "SimpleAttrs"}},
                                {
                                    "name": "list_of_dict_field",
                                    "type": {"type": "array", "items": {"type": "map", "values": "long"}},
                                },
                                {
                                    "name": "dict_of_list_field",
                                    "type": {"type": "map", "values": {"type": "array", "items": "long"}},
                                },
                            ],
                        },
                    }
                ],
            },
        ),
    )
    @ddt.unpack
    def test_schema_string(self, data_cls, expected_schema):
        """
        Test JSON round-trip; schema creation is tested more fully in test_schema.py.
        """
        SIGNAL = create_simple_signal({
            "data": data_cls
        })

        actual_schema = json.loads(AvroSignalDeserializer(SIGNAL).schema_string())

        assert actual_schema == expected_schema

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
        expected_event_data = EventData("foo", "bar.course",
                                        SubTestData0("a.sub.name", "a.nother.course"),
                                        SubTestData1("b.uber.sub.name", "b.uber.another.course")
                                        )
        test_data = event_data["test_data"]
        self.assertIsInstance(test_data, EventData)
        self.assertEqual(test_data, expected_event_data)

    def test_default_datetime_deserialization(self):
        SIGNAL = create_simple_signal({"birthday": datetime})
        deserializer = AvroSignalDeserializer(SIGNAL)
        birthday = datetime(year=1989, month=9, day=6)
        as_dict = {"birthday": birthday.isoformat()}
        event_data = deserializer.from_dict(as_dict)
        birthday_deserialized = event_data["birthday"]
        self.assertIsInstance(birthday_deserialized, datetime)
        self.assertEqual(birthday_deserialized, birthday)

    def test_default_coursekey_deserialization(self):
        SIGNAL = create_simple_signal({"course": CourseKey})
        deserializer = AvroSignalDeserializer(SIGNAL)
        course_key = CourseKey.from_string("course-v1:edX+DemoX.1+2014")
        as_dict = {"course": str(course_key)}
        event_data = deserializer.from_dict(as_dict)
        course_deserialized = event_data["course"]
        self.assertIsInstance(course_deserialized, CourseKey)
        self.assertEqual(course_deserialized, course_key)

    def test_default_usagekey_deserialization(self):
        """
        Test deserialization of UsageKey
        """
        SIGNAL = create_simple_signal({"usage_key": UsageKey})
        deserializer = AvroSignalDeserializer(SIGNAL)
        usage_key = UsageKey.from_string(
            "block-v1:edx+DemoX+Demo_course+type@video+block@UaEBjyMjcLW65gaTXggB93WmvoxGAJa0JeHRrDThk",
        )
        as_dict = {"usage_key": str(usage_key)}
        event_data = deserializer.from_dict(as_dict)
        usage_key_deserialized = event_data["usage_key"]
        self.assertIsInstance(usage_key_deserialized, UsageKey)
        self.assertEqual(usage_key_deserialized, usage_key)

    def test_default_librarylocatorv2_deserialization(self):
        """
        Test deserialization of LibraryLocatorV2
        """
        SIGNAL = create_simple_signal({"library_key": LibraryLocatorV2})
        deserializer = AvroSignalDeserializer(SIGNAL)
        library_key = LibraryLocatorV2.from_string("lib:MITx:reallyhardproblems")
        as_dict = {"library_key": str(library_key)}
        event_data = deserializer.from_dict(as_dict)
        library_key_deserialized = event_data["library_key"]
        self.assertIsInstance(library_key_deserialized, LibraryLocatorV2)
        self.assertEqual(library_key_deserialized, library_key)

    def test_default_libraryusagelocatorv2_deserialization(self):
        """
        Test deserialization of LibraryUsageLocatorV2
        """
        SIGNAL = create_simple_signal({"usage_key": LibraryUsageLocatorV2})
        deserializer = AvroSignalDeserializer(SIGNAL)
        usage_key = LibraryUsageLocatorV2.from_string("lb:MITx:reallyhardproblems:problem:problem1")
        as_dict = {"usage_key": str(usage_key)}
        event_data = deserializer.from_dict(as_dict)
        usage_key_deserialized = event_data["usage_key"]
        self.assertIsInstance(usage_key_deserialized, LibraryUsageLocatorV2)
        self.assertEqual(usage_key_deserialized, usage_key)

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
        self.assertEqual(data_dict["data"], SimpleAttrsWithDefaults())

    def test_deserialization_of_nested_optional_fields(self):
        SIGNAL = create_simple_signal({
            "data": NestedAttrsWithDefaults
        })
        deserializer = AvroSignalDeserializer(SIGNAL)
        as_dict = {"data": {"field_0": {}}}
        data_dict = deserializer.from_dict(as_dict)
        nested_field = data_dict["data"].field_0
        self.assertIsInstance(nested_field, SimpleAttrsWithDefaults)
        self.assertEqual(nested_field, SimpleAttrsWithDefaults())

    def test_deserialization_of_list_with_annotation(self):
        """
        Check that deserialization works as expected when list data is annotated.
        """
        LIST_SIGNAL = create_simple_signal({"list_input": List[int]})
        initial_dict = {"list_input": [1, 3]}
        deserializer = AvroSignalDeserializer(LIST_SIGNAL)
        event_data = deserializer.from_dict(initial_dict)
        expected_event_data = [1, 3]
        test_data = event_data["list_input"]
        self.assertIsInstance(test_data, list)
        self.assertEqual(test_data, expected_event_data)

    def test_deserialization_of_list_without_annotation(self):
        """
        Check that deserialization raises error when list data is not annotated.
        """
        # create dummy signal to bypass schema check while initializing deserializer
        # This allows us to test whether correct exceptions are raised while deserializing data
        SIGNAL = create_simple_signal({"list_input": List[int]})
        LIST_SIGNAL = create_simple_signal({"list_input": List})
        initial_dict = {"list_input": [1, 3]}
        deserializer = AvroSignalDeserializer(SIGNAL)
        # Update signal with incomplete type info
        deserializer.signal = LIST_SIGNAL
        with self.assertRaises(TypeError):
            deserializer.from_dict(initial_dict)

    def test_deserialization_of_dict_with_annotation(self):
        """
        Check that deserialization works as expected when dict data is annotated.
        """
        DICT_SIGNAL = create_simple_signal({"dict_input": Dict[str, int]})
        initial_dict = {"dict_input": {"key1": 1, "key2": 3}}

        deserializer = AvroSignalDeserializer(DICT_SIGNAL)
        event_data = deserializer.from_dict(initial_dict)
        expected_event_data = {"key1": 1, "key2": 3}
        test_data = event_data["dict_input"]

        self.assertIsInstance(test_data, dict)
        self.assertEqual(test_data, expected_event_data)

    def test_deserialization_of_dict_of_lists(self):
        SIGNAL = create_simple_signal({"dict_input": dict[str, List[int]]})
        initial_dict = {"dict_input": {"key1": [1, 2], "key2": [3, 4]}}

        deserializer = AvroSignalDeserializer(SIGNAL)
        event_data = deserializer.from_dict(initial_dict)
        expected_event_data = {"key1": [1, 2], "key2": [3, 4]}
        test_data = event_data["dict_input"]

        self.assertIsInstance(test_data, dict)
        self.assertEqual(test_data, expected_event_data)

    def test_deserialization_of_dict_of_event_data(self):
        SIGNAL = create_simple_signal({"dict_input": dict[str, EventData]})
        initial_dict = {
            "dict_input": {
                "key1": {
                    "course_id": "bar",
                    "sub_name": "bar.name",
                    "sub_test_0": {"course_id": "bar1.course", "sub_name": "bar1.name"},
                    "sub_test_1": {"course_id": "bar2.course", "sub_name": "bar2.name"},
                },
                "key2": {
                    "course_id": "foo",
                    "sub_name": "foo.name",
                    "sub_test_0": {"course_id": "foo1.course", "sub_name": "foo1.name"},
                    "sub_test_1": {"course_id": "foo2.course", "sub_name": "foo2.name"},
                },
            }
        }

        deserializer = AvroSignalDeserializer(SIGNAL)
        event_data = deserializer.from_dict(initial_dict)
        expected_event_data = {
            "key1": EventData(
                sub_name="bar.name",
                course_id="bar",
                sub_test_0=SubTestData0(sub_name="bar1.name", course_id="bar1.course"),
                sub_test_1=SubTestData1(sub_name="bar2.name", course_id="bar2.course"),
            ),
            "key2": EventData(
                sub_name="foo.name",
                course_id="foo",
                sub_test_0=SubTestData0(sub_name="foo1.name", course_id="foo1.course"),
                sub_test_1=SubTestData1(sub_name="foo2.name", course_id="foo2.course"),
            ),
        }
        test_data = event_data["dict_input"]

        self.assertIsInstance(test_data, dict)
        self.assertEqual(test_data, expected_event_data)

    def test_deserialization_of_list_of_dicts(self):
        SIGNAL = create_simple_signal({"list_input": List[dict[str, int]]})
        initial_dict = {"list_input": [{"key1": 1, "key2": 2}, {"key1": 3, "key2": 4}]}

        deserializer = AvroSignalDeserializer(SIGNAL)
        event_data = deserializer.from_dict(initial_dict)
        expected_event_data = [{"key1": 1, "key2": 2}, {"key1": 3, "key2": 4}]
        test_data = event_data["list_input"]

        self.assertIsInstance(test_data, list)
        self.assertEqual(test_data, expected_event_data)

    def test_deserialization_of_list_of_event_data(self):
        SIGNAL = create_simple_signal({"list_input": List[EventData]})
        initial_dict = {
            "list_input": [
                {
                    "course_id": "bar",
                    "sub_name": "bar.name",
                    "sub_test_0": {"course_id": "bar1.course", "sub_name": "bar1.name"},
                    "sub_test_1": {"course_id": "bar2.course", "sub_name": "bar2.name"},
                },
                {
                    "course_id": "foo",
                    "sub_name": "foo.name",
                    "sub_test_0": {"course_id": "foo1.course", "sub_name": "foo1.name"},
                    "sub_test_1": {"course_id": "foo2.course", "sub_name": "foo2.name"},
                },
            ]
        }

        deserializer = AvroSignalDeserializer(SIGNAL)
        event_data = deserializer.from_dict(initial_dict)
        expected_event_data = [
            EventData(
                sub_name="bar.name",
                course_id="bar",
                sub_test_0=SubTestData0(sub_name="bar1.name", course_id="bar1.course"),
                sub_test_1=SubTestData1(sub_name="bar2.name", course_id="bar2.course"),
            ),
            EventData(
                sub_name="foo.name",
                course_id="foo",
                sub_test_0=SubTestData0(sub_name="foo1.name", course_id="foo1.course"),
                sub_test_1=SubTestData1(sub_name="foo2.name", course_id="foo2.course"),
            ),
        ]
        test_data = event_data["list_input"]

        self.assertIsInstance(test_data, list)
        self.assertEqual(test_data, expected_event_data)

    def test_deserialization_of_dict_without_annotation(self):
        """
        Check that deserialization raises error when dict data is not annotated.

        Create dummy signal to bypass schema check while initializing deserializer. Then,
        update signal with incomplete type info to test whether correct exceptions are raised while deserializing data.
        """
        SIGNAL = create_simple_signal({"dict_input": Dict[str, int]})
        DICT_SIGNAL = create_simple_signal({"dict_input": Dict})
        initial_dict = {"dict_input": {"key1": 1, "key2": 3}}

        deserializer = AvroSignalDeserializer(SIGNAL)
        deserializer.signal = DICT_SIGNAL

        with self.assertRaises(TypeError):
            deserializer.from_dict(initial_dict)

    def test_deserialization_of_dicts_with_keys_of_complex_types_fails(self):
        SIGNAL = create_simple_signal({"dict_input": Dict[CourseKey, int]})
        deserializer = AvroSignalDeserializer(SIGNAL)
        initial_dict = {"dict_input": {CourseKey.from_string("course-v1:edX+DemoX.1+2014"): 1}}
        with self.assertRaises(TypeError):
            deserializer.from_dict(initial_dict)

    def test_deserialization_of_unsupported_data_type(self):
        """
        Check that deserialization raises TypeError when encountering an unsupported data type.

        Create a dummy signal with a custom class that isn't in the deserializers dictionary
        and doesn't have __attrs_attrs__ to test the final TypeError case.
        """
        # Create a custom class that isn't in the deserializers and doesn't have __attrs_attrs__
        class CustomUnsupportedType:
            pass

        # Create a signal with a valid type first to avoid schema validation errors
        VALID_SIGNAL = create_simple_signal({"list_input": List[int]})
        INVALID_SIGNAL = create_simple_signal({"list_input": List[CustomUnsupportedType]})
        initial_dict = {"list_input": [1, 2, 3]}
        deserializer = AvroSignalDeserializer(VALID_SIGNAL)
        # Update signal with invalid type
        deserializer.signal = INVALID_SIGNAL

        # Test that it raises TypeError with appropriate message
        with self.assertRaises(TypeError) as context:
            deserializer.from_dict(initial_dict)

        # Verify the error message mentions the unsupported type
        self.assertIn("Unable to deserialize", str(context.exception))
        self.assertIn("CustomUnsupportedType", str(context.exception))

    def test_deserialize_bytes_to_event_data(self):
        """
        Test deserialize_bytes_to_event_data utility function.
        """
        SIGNAL = create_simple_signal({"test_data": EventData})
        bytes_data = b'\x06foo\x14bar.course\x14a.sub.name\x1ea.nother.course\x1eb.uber.sub.name*b.uber.another.course'
        expected = {"test_data": EventData(
            "foo",
            "bar.course",
            SubTestData0("a.sub.name", "a.nother.course"),
            SubTestData1("b.uber.sub.name", "b.uber.another.course"),
        )}
        deserialized = deserialize_bytes_to_event_data(bytes_data, SIGNAL)
        self.assertIsInstance(deserialized["test_data"], EventData)
        self.assertEqual(deserialized, expected)

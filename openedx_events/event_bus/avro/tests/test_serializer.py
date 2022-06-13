"""Tests for avro.serializer module."""

from datetime import datetime
from unittest import TestCase

from opaque_keys.edx.keys import CourseKey

from openedx_events.event_bus.avro.serializer import AvroSignalSerializer
from openedx_events.event_bus.avro.tests.test_utilities import (
    EventData,
    NestedAttrsWithDefaults,
    NestedNonAttrs,
    NonAttrs,
    SimpleAttrsWithDefaults,
    SpecialSerializer,
    SubTestData0,
    SubTestData1,
    create_simple_signal,
)


class TestAvroSignalSerializer(TestCase):
    """Tests for AvroSignalSerializer."""

    def test_convert_event_data_to_dict(self):
        """
        Tests that an event with complex attrs objects can be converted to a dict.
        """

        # A test record that we can try to serialize to avro.
        test_data = EventData(
            "foo",
            "bar.course",
            SubTestData0("a.sub.name", "a.nother.course"),
            SubTestData1("b.uber.sub.name", "b.uber.another.course"),
        )
        SIGNAL = create_simple_signal({"test_data": EventData})

        serializer = AvroSignalSerializer(SIGNAL)

        data_dict = serializer.to_dict({"test_data": test_data})
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

    def test_default_datetime_serialization(self):
        SIGNAL = create_simple_signal({"birthday": datetime})
        serializer = AvroSignalSerializer(SIGNAL)
        birthday = datetime(year=1989, month=9, day=6)
        test_data = {"birthday": birthday}
        data_dict = serializer.to_dict(test_data)
        self.assertDictEqual(data_dict, {"birthday": birthday.isoformat()})

    def test_default_coursekey_serialization(self):
        SIGNAL = create_simple_signal({"course": CourseKey})
        serializer = AvroSignalSerializer(SIGNAL)
        course_key = CourseKey.from_string("course-v1:edX+DemoX.1+2014")
        test_data = {"course": course_key}
        data_dict = serializer.to_dict(test_data)
        self.assertDictEqual(data_dict, {"course": str(course_key)})

    def test_serialization_with_custom_serializer(self):
        SIGNAL = create_simple_signal({"test_data": NonAttrs})

        serializer = SpecialSerializer(SIGNAL)
        test_data = {
            "test_data": NonAttrs("a.val", "a.nother.val")
        }
        data_dict = serializer.to_dict(test_data)
        self.assertDictEqual(data_dict, {"test_data": "a.val:a.nother.val"})

    def test_serialization_with_custom_serializer_on_nested_fields(self):
        SIGNAL = create_simple_signal({"test_data": NestedNonAttrs})
        test_data = {
            "test_data": NestedNonAttrs(field_0=NonAttrs("a.val", "a.nother.val"))
        }
        serializer = SpecialSerializer(SIGNAL)
        test_data = {"test_data": NestedNonAttrs(field_0=NonAttrs("a.val", "a.nother.val"))}
        data_dict = serializer.to_dict(test_data)
        self.assertDictEqual(data_dict, {"test_data": {
            "field_0": "a.val:a.nother.val"
        }})

    def test_serialization_of_optional_fields(self):
        SIGNAL = create_simple_signal({
            "data": SimpleAttrsWithDefaults
        })
        serializer = AvroSignalSerializer(SIGNAL)
        event_data = {"data": SimpleAttrsWithDefaults()}
        data_dict = serializer.to_dict(event_data)
        self.assertDictEqual(data_dict, {"data": {'boolean_field': None,
                                                  'bytes_field': None,
                                                  'float_field': None,
                                                  'int_field': None,
                                                  'string_field': None,
                                                  'attrs_field': None}})

    def test_serialization_of_nested_optional_fields(self):
        SIGNAL = create_simple_signal({
            "data": NestedAttrsWithDefaults
        })
        serializer = AvroSignalSerializer(SIGNAL)

        event_data = {"data": NestedAttrsWithDefaults(field_0=SimpleAttrsWithDefaults())}
        data_dict = serializer.to_dict(event_data)
        self.assertDictEqual(data_dict, {"data": {"field_0": {'boolean_field': None,
                                                              'bytes_field': None,
                                                              'float_field': None,
                                                              'int_field': None,
                                                              'string_field': None,
                                                              'attrs_field': None
                                                              }}})

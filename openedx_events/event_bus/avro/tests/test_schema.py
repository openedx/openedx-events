"""
Tests for event_bus.avro.schema module
"""
from typing import List
from unittest import TestCase

from openedx_events.event_bus.avro.schema import schema_from_signal
from openedx_events.event_bus.avro.tests.test_utilities import (
    EventData,
    NestedAttrsWithDefaults,
    NestedNonAttrs,
    NonAttrs,
    SimpleAttrs,
    SimpleAttrsWithDefaults,
    SubTestData0,
    SubTestData1,
    create_simple_signal,
)


class TestSchemaGeneration(TestCase):
    """
    Test Avro schema generation.
    """

    def setUp(self) -> None:
        super().setUp()
        self.maxDiff = None

    def test_simple_schema_generation(self):
        SIGNAL = create_simple_signal({"event_data": SimpleAttrs})
        schema = schema_from_signal(SIGNAL)
        expected_dict = {
            "type": "record",
            "name": "CloudEvent",
            "doc": "Avro Event Format for CloudEvents created with openedx_events/schema",
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

        self.assertDictEqual(schema, expected_dict)

    def test_nested_attrs_object_serialization(self):
        SIGNAL = create_simple_signal({"test_data": EventData})
        schema = schema_from_signal(SIGNAL)

        expected_dict = {
            "type": "record",
            "name": "CloudEvent",
            "doc": "Avro Event Format for CloudEvents created with openedx_events/schema",
            "fields": [
                {"name": "test_data", "type":
                    {"name": "EventData", "type": "record", "fields": [
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

        self.assertDictEqual(schema, expected_dict)

    def test_multiple_top_level_fields(self):
        SIGNAL = create_simple_signal({
            "top_level_key_0": SubTestData0,
            "top_level_key_1": SubTestData1,
        })
        schema = schema_from_signal(SIGNAL)

        expected_dict = {
            "type": "record",
            "name": "CloudEvent",
            "doc": "Avro Event Format for CloudEvents created with openedx_events/schema",
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
        self.assertDictEqual(schema, expected_dict)

    def test_schema_for_custom_type(self):
        SIGNAL = create_simple_signal({"test_data": NonAttrs})
        expected_dict = {
            "type": "record",
            "name": "CloudEvent",
            "doc": "Avro Event Format for CloudEvents created with openedx_events/schema",
            "fields": [
                {"name": "test_data", "type": "string"}
            ],
        }
        schema = schema_from_signal(SIGNAL, custom_type_to_avro_type={NonAttrs: "string"})
        self.assertDictEqual(schema, expected_dict)

    def test_schema_for_nested_custom_type(self):
        SIGNAL = create_simple_signal({"test_data": NestedNonAttrs})
        expected_dict = {
            "type": "record",
            "name": "CloudEvent",
            "doc": "Avro Event Format for CloudEvents created with openedx_events/schema",
            "fields": [
                {"name": "test_data", "type": {
                    "name": "NestedNonAttrs",
                    "type": "record",
                    "fields": [
                        {'name': 'field_0', 'type': 'string'}
                    ]
                }}
            ],
        }
        schema = schema_from_signal(SIGNAL, custom_type_to_avro_type={NonAttrs: "string"})
        self.assertDictEqual(schema, expected_dict)

    def test_schema_for_types_with_defaults(self):
        SIGNAL = create_simple_signal({"test_data": SimpleAttrsWithDefaults})
        expected_dict = {
            "type": "record",
            "name": "CloudEvent",
            "doc": "Avro Event Format for CloudEvents created with openedx_events/schema",
            "fields": [
                {"name": "test_data", "type":
                    {"name": "SimpleAttrsWithDefaults", "type": "record", "fields": [
                        {"name": "boolean_field", "type": ["null", "boolean"], "default": None},
                        {"name": "int_field", "type": ["null", "long"], "default": None},
                        {"name": "float_field", "type": ["null", "double"], "default": None},
                        {"name": "bytes_field", "type": ["null", "bytes"], "default": None},
                        {"name": "string_field", "type": ["null", "string"], "default": None},
                        {"name": "attrs_field", "default": None,
                         "type": ["null",
                                  {"name": "SimpleAttrs", "type": "record", "fields": [
                                      {"name": "boolean_field", "type": "boolean"},
                                      {"name": "int_field", "type": "long"},
                                      {"name": "float_field", "type": "double"},
                                      {"name": "bytes_field", "type": "bytes"},
                                      {"name": "string_field", "type": "string"},
                                  ]
                                   }]}
                    ]}
                 }
            ],
        }
        schema = schema_from_signal(SIGNAL)
        self.assertDictEqual(schema, expected_dict)

    def test_schema_for_types_with_nested_defaults(self):
        SIGNAL = create_simple_signal({"test_data": NestedAttrsWithDefaults})
        expected_dict = {
            'name': 'CloudEvent',
            'type': 'record',
            'doc': 'Avro Event Format for CloudEvents created with openedx_events/schema',
            'fields': [{
                'name': 'test_data',
                'type': {
                    'name': 'NestedAttrsWithDefaults',
                    'type': 'record',
                    'fields': [{
                        'name': 'field_0',
                        'type': {
                            'name': 'SimpleAttrsWithDefaults',
                            'type': 'record',
                            'fields': [
                                {'name': 'boolean_field', 'type': ['null', 'boolean'], 'default': None},
                                {'name': 'int_field', 'type': ['null', 'long'], 'default': None},
                                {'name': 'float_field', 'type': ['null', 'double'], 'default': None},
                                {'name': 'bytes_field', 'type': ['null', 'bytes'], 'default': None},
                                {'name': 'string_field', 'type': ['null', 'string'], 'default': None},
                                {'name': 'attrs_field', 'default': None,
                                 'type': ['null', {
                                     'name': 'SimpleAttrs',
                                     'type': 'record',
                                     'fields': [
                                         {'name': 'boolean_field', 'type': 'boolean'},
                                         {'name': 'int_field', 'type': 'long'},
                                         {'name': 'float_field', 'type': 'double'},
                                         {'name': 'bytes_field', 'type': 'bytes'},
                                         {'name': 'string_field', 'type': 'string'
                                          }]
                                 }],
                                 }]
                        }
                    }]
                }
            }]
        }
        schema = schema_from_signal(SIGNAL, custom_type_to_avro_type={NonAttrs: "string"})
        self.assertDictEqual(schema, expected_dict)

    def test_throw_exception_on_unextended_custom_type(self):
        class UnextendedClass:
            pass

        SIGNAL = create_simple_signal({"unextended_class": UnextendedClass})
        with self.assertRaises(TypeError):
            schema_from_signal(SIGNAL)

    def test_throw_exception_to_list_or_dict_types_without_annotation(self):
        LIST_SIGNAL = create_simple_signal({"list_input": list})
        DICT_SIGNAL = create_simple_signal({"list_input": dict})
        with self.assertRaises(Exception):
            schema_from_signal(LIST_SIGNAL)

        with self.assertRaises(Exception):
            schema_from_signal(DICT_SIGNAL)

    def test_list_with_annotation_works(self):
        LIST_SIGNAL = create_simple_signal({"list_input": List[int]})
        expected_dict = {
            'name': 'CloudEvent',
            'type': 'record',
            'doc': 'Avro Event Format for CloudEvents created with openedx_events/schema',
            'fields': [{
                'name': 'list_input',
                'type': {'type': 'array', 'items': 'long'},
            }],
        }
        schema = schema_from_signal(LIST_SIGNAL)
        self.assertDictEqual(schema, expected_dict)

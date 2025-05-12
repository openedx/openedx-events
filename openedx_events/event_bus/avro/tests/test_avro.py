"""Test interplay of the various Avro helper classes"""
import io
import os
from datetime import datetime
from typing import List, Union
from unittest import TestCase
from uuid import UUID, uuid4

from ccx_keys.locator import CCXLocator
from fastavro import schemaless_reader, schemaless_writer
from fastavro.repository.base import SchemaRepositoryError
from fastavro.schema import load_schema
from opaque_keys.edx.keys import CourseKey, UsageKey
from opaque_keys.edx.locator import (
    LibraryCollectionLocator,
    LibraryContainerLocator,
    LibraryLocatorV2,
    LibraryUsageLocatorV2,
)

from openedx_events.event_bus.avro.deserializer import AvroSignalDeserializer, deserialize_bytes_to_event_data
from openedx_events.event_bus.avro.serializer import AvroSignalSerializer, serialize_event_data_to_bytes
from openedx_events.event_bus.avro.tests.test_utilities import (
    EventData,
    NestedAttrsWithDefaults,
    SimpleAttrsWithDefaults,
    SubTestData0,
    SubTestData1,
    create_simple_signal,
)
from openedx_events.tests.utils import FreezeSignalCacheMixin
from openedx_events.tooling import KNOWN_UNSERIALIZABLE_SIGNALS, OpenEdxPublicSignal, load_all_signals


def generate_test_data_for_schema(schema):  # pragma: no cover
    """
    Generates a test data dict for the given schema.

    Arguments:
        schema: A JSON representation of an Avro schema

    Returns:
         A dictionary of test data parseable by the schema
    """
    defaults_per_type = {
        'long': 1,
        'boolean': True,
        'string': "default",
        'double': 1.0,
        'null': None,
        'map': {'key': 'value'},
    }

    def get_default_value_or_raise(schema_field_type):
        try:
            return defaults_per_type[schema_field_type]
        # 'None' is the default value for type=null so we can't just check if default_value is not None
        except KeyError as exc:
            raise Exception(f"Unsupported type {schema_field_type}") from exc  # pylint: disable=broad-exception-raised

    data_dict = {}
    top_level = schema['fields']
    for field in top_level:
        key = field['name']
        field_type = field['type']

        # some fields (like optional ones) accept multiple types. Choose the first one and run with it.
        if isinstance(field_type, list):
            field_type = field_type[0]

        # if the field_type is a dict, we're either dealing with a list or a custom object
        if isinstance(field_type, dict):
            sub_field_type = field_type['type']
            if sub_field_type == "array":
                # if we're dealing with a list, "items" will be the type of items in the list
                data_dict.update({key: [get_default_value_or_raise(field_type['items'])]})
            elif sub_field_type == "record":
                # if we're dealing with a record, recurse into the record
                data_dict.update({key: generate_test_data_for_schema(field_type)})
            elif sub_field_type == "map":
                # if we're dealing with a map, "values" will be the type of values in the map
                data_dict.update({key: {"key": get_default_value_or_raise(field_type["values"])}})
            else:
                raise Exception(f"Unsupported type {field_type}")  # pylint: disable=broad-exception-raised

        # a record is a collection of fields rather than a field itself, so recursively generate and add each field
        elif field_type == "record":
            data_dict.update([generate_test_data_for_schema(sub_field) for sub_field in field['fields']])
        else:
            data_dict.update({key: get_default_value_or_raise(field_type)})

    return data_dict


def generate_test_event_data_for_data_type(data_type):  # pragma: no cover
    """
    Generates test data for use in the event bus test cases.

    Builds data by filling in dummy data for basic data types (int/float/bool/str)
    and recursively breaks down the classes for nested classes into basic data types.

    Arguments:
        data_type: The type of the data which we are generating data for

    Returns:
        (dict): A data dictionary containing dummy data for all attributes of the class
    """
    defaults_per_type = {
        int: 1,
        bool: True,
        str: "default",
        float: 1.0,
        CourseKey: CourseKey.from_string("course-v1:edX+DemoX.1+2014"),
        UsageKey: UsageKey.from_string(
            "block-v1:edx+DemoX+Demo_course+type@video+block@UaEBjyMjcLW65gaTXggB93WmvoxGAJa0JeHRrDThk",
        ),
        LibraryCollectionLocator: LibraryCollectionLocator.from_string('lib-collection:MITx:reallyhardproblems:col1'),
        LibraryContainerLocator: LibraryContainerLocator.from_string(
            'lct:MITx:reallyhardproblems:unit:test-container',
        ),
        LibraryLocatorV2: LibraryLocatorV2.from_string('lib:MITx:reallyhardproblems'),
        LibraryUsageLocatorV2: LibraryUsageLocatorV2.from_string('lb:MITx:reallyhardproblems:problem:problem1'),
        List[int]: [1, 2, 3],
        List[str]: ["hi", "there"],
        datetime: datetime.now(),
        CCXLocator: CCXLocator(org='edx', course='DemoX', run='Demo_course', ccx='1'),
        UUID: uuid4(),
        dict[str, str]: {'key': 'value'},
        dict[str, int]: {'key': 1},
        dict[str, float]: {'key': 1.0},
        dict[str, bool]: {'key': True},
        dict[str, CourseKey]: {'key': CourseKey.from_string("course-v1:edX+DemoX.1+2014")},
        dict[str, UsageKey]: {'key': UsageKey.from_string(
            "block-v1:edx+DemoX+Demo_course+type@video+block@UaEBjyMjcLW65gaTXggB93WmvoxGAJa0JeHRrDThk",
        )},
        dict[str, LibraryLocatorV2]: {'key': LibraryLocatorV2.from_string('lib:MITx:reallyhardproblems')},
        dict[str, LibraryCollectionLocator]: {
            'key': LibraryCollectionLocator.from_string('lib-collection:MITx:reallyhardproblems:col1'),
        },
        dict[str, LibraryContainerLocator]: {
            'key': LibraryContainerLocator.from_string('lct:MITx:reallyhardproblems:unit:test-container'),
        },
        dict[str, LibraryUsageLocatorV2]: {
            'key': LibraryUsageLocatorV2.from_string('lb:MITx:reallyhardproblems:problem:problem1'),
        },
        dict[str, List[int]]: {'key': [1, 2, 3]},
        dict[str, List[str]]: {'key': ["hi", "there"]},
        dict[str, dict[str, str]]: {'key': {'key': 'value'}},
        dict[str, dict[str, int]]: {'key': {'key': 1}},
        dict[str, Union[str, int]]: {'key': 'value'},
        dict[str, Union[str, int, float]]: {'key': 1.0},
    }
    data_dict = {}
    for attribute in data_type.__attrs_attrs__:
        result = defaults_per_type.get(attribute.type, None)
        if result is not None:
            data_dict.update({attribute.name: result})
        elif attribute.type in [dict, list]:
            # pylint: disable-next=broad-exception-raised
            raise Exception("Unable to generate Avro schema for dict or array fields")
        else:
            data_dict.update({attribute.name: attribute.type(**generate_test_event_data_for_data_type(attribute.type))})
    return data_dict


def generate_test_data_for_signal(signal: OpenEdxPublicSignal) -> dict:
    """
    Generates test data for use in the event bus test cases.

    Builds data by filling in dummy data for basic data types (int/float/bool/str)
    and recursively breaks down the classes for nested classes into basic data types.

    Arguments:
        data_type: The type of the data which we are generating data for

    Returns:
        (dict): A data dictionary containing dummy data for all attributes of the class
    """
    test_data = {}
    for key, curr_class in signal.init_data.items():
        example_data = generate_test_event_data_for_data_type(curr_class)
        example_data_processed = curr_class(**example_data)
        test_data.update({key: example_data_processed})
    return test_data


class TestAvro(FreezeSignalCacheMixin, TestCase):
    """Tests for end-to-end serialization and deserialization of events and schema evolution"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Ensure we can usefully call all_events()
        load_all_signals()

    def test_all_events(self):
        for signal in OpenEdxPublicSignal.all_events():
            if signal.event_type in KNOWN_UNSERIALIZABLE_SIGNALS:
                continue
            test_data = generate_test_data_for_signal(signal)
            serializer = AvroSignalSerializer(signal)
            serialized = serializer.to_dict(test_data)
            deserializer = AvroSignalDeserializer(signal)
            deserialized = deserializer.from_dict(serialized)
            self.assertDictEqual(deserialized, test_data)

    def test_evolution_is_forward_compatible(self):
        """
        Test current version of events is forward compatible with stored schemas.

        There's no assert because as long as the test doesn't raise an error, the new schema is
        forward-compatible with the original.
        """
        for signal in OpenEdxPublicSignal.all_events():
            if signal.event_type in KNOWN_UNSERIALIZABLE_SIGNALS:
                continue
            test_data = generate_test_data_for_signal(signal)
            serializer = AvroSignalSerializer(signal)
            schema_dict = serializer.schema

            # write to bytes using current schema
            current_out = io.BytesIO()
            data_dict = serializer.to_dict(test_data)
            schemaless_writer(current_out, schema_dict, data_dict)
            current_out.seek(0)
            current_event_bytes = current_out.read()

            # get stored schema
            schema_filename = f"{os.path.dirname(os.path.abspath(__file__))}/schemas/" \
                              f"{signal.event_type.replace('.', '+')}_schema.avsc"
            try:
                stored_schema = load_schema(schema_filename)
            except SchemaRepositoryError:  # pragma: no cover
                self.fail(f"Missing file {schema_filename}. If a new signal has been added, you may need to run the"
                          f" generate_avro_schemas management command to save the signal schema.")

            data_file_current = io.BytesIO(current_event_bytes)

            # read bytes using stored schema
            schemaless_reader(data_file_current, reader_schema=stored_schema, writer_schema=schema_dict)

    def test_evolution_is_backward_compatible(self):
        """
        Test current version of events is backward compatible with stored schemas.

        There's no assert because as long as the test doesn't raise an error, the new schema is
        backward-compatible with the original.

        Caveat: While we can go from an attrs class to a schema, we cannot go from a schema to an attrs class in the
        same way because of custom serializers. Thus, when we are generating test data, we can only generate
        the dictionary we would get after calling schema.to_dict.
        """
        for signal in OpenEdxPublicSignal.all_events():
            if signal.event_type in KNOWN_UNSERIALIZABLE_SIGNALS:
                continue
            serializer = AvroSignalSerializer(signal)
            schema_dict = serializer.schema

            # get stored schema
            schema_filename = f"{os.path.dirname(os.path.abspath(__file__))}/schemas/" \
                              f"{signal.event_type.replace('.', '+')}_schema.avsc"
            try:
                old_schema = load_schema(schema_filename)
            except SchemaRepositoryError:  # pragma: no cover
                self.fail(f"Missing file {schema_filename}. If a new signal has been added, you may need to run the"
                          f" generate_avro_schemas management command to save the signal schema.")
            data_dict = generate_test_data_for_schema(old_schema)

            # write to bytes using stored schema
            stored_out = io.BytesIO()
            schemaless_writer(stored_out, old_schema, data_dict)
            stored_out.seek(0)
            stored_event_bytes = stored_out.read()

            data_file_stored = io.BytesIO(stored_event_bytes)

            # read bytes using current schema
            schemaless_reader(data_file_stored, reader_schema=schema_dict, writer_schema=old_schema)

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

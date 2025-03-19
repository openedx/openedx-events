"""Test interplay of the various Avro helper classes"""
import io
import os
from datetime import datetime
from typing import Any, List, Union, get_args, get_origin
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


def generate_test_data_for_schema(schema: dict[str, Any]) -> dict:
    """
    Generates test data dict for the given schema.

    This function creates sample data that conforms to the provided Avro schema
    structure. It handles complex nested schemas including records, arrays,
    maps, unions, and references to named types. For each field, it generates
    sample data according to the field type.

    Args:
        schema (dict[str, Any]): The Avro schema as a dictionary

    Returns:
        dict: Test data according to the schema
    """
    DEFAULT_PER_TYPE = {
        "long": 1,
        "boolean": True,
        "string": "default",
        "double": 1.0,
        "null": None,
    }

    # Repository for defined types in the schema
    defined_types = {}

    def register_defined_types(schema_obj: Any) -> None:
        """
        Registers all types defined in the schema for later reference.

        Args:
            schema_obj (Any): A schema object which might be a dict, list,
                or primitive
        """
        if isinstance(schema_obj, dict):
            if schema_obj.get("type") == "record" and "name" in schema_obj:
                record_name = schema_obj["name"]
                defined_types[record_name] = schema_obj

                # Process fields to find more defined types
                for field in schema_obj.get("fields", []):
                    field_type = field.get("type")
                    register_defined_types(field_type)

            # Process arrays and maps
            elif schema_obj.get("type") == "array":
                register_defined_types(schema_obj.get("items"))
            elif schema_obj.get("type") == "map":
                register_defined_types(schema_obj.get("values"))

    def process_schema(schema_obj: Any) -> Any:
        """
        Processes a complete schema and generates test data. This is the entry
        point for processing.

        Args:
            schema_obj (Any): The schema object to process

        Returns:
            Generated test data for the schema
        """
        # First, we register the types defined throughout the schema
        register_defined_types(schema_obj)

        # Then, we process the schema to generate data
        if isinstance(schema_obj, dict) and schema_obj.get("type") == "record":
            return process_record(schema_obj)
        else:
            return process_type(schema_obj)

    def process_record(record_schema: dict[str, Any]) -> dict[str, Any]:
        """
        Args:
            record_schema (dict[str, Any]): A record type schema

        Returns:
            A dictionary with all fields populated according to the schema
        """
        result = {}
        for field in record_schema.get("fields", []):
            field_name = field.get("name")
            field_type = field.get("type")

            # Process the field type
            result[field_name] = process_type(field_type)

        return result

    def process_type(type_spec: Any) -> Any:
        """
        Processes any data type in Avro and generates an appropriate test value.
        Handles primitive types, complex types, union types, and references to
        defined types.

        Args:
            type_spec (Any): A type specification which might be a string,
                dict, or list

        Returns:
            An appropriate test value for the specified type
        """
        # Primitive types like string, long, boolean, etc.
        if isinstance(type_spec, str):
            if type_spec in DEFAULT_PER_TYPE:
                return DEFAULT_PER_TYPE[type_spec]

            # It's a reference to a previously defined type
            if type_spec in defined_types:
                return process_type(defined_types[type_spec])

            return {}

        # Union types (list of possible types)
        if isinstance(type_spec, list):
            # If null is in the list, we try to return a non-null type
            if "null" in type_spec:
                for t in type_spec:
                    if t != "null":
                        return process_type(t)
                # If all types are null, we return None
                return None

            # If there's no null, we use the first type
            if type_spec:
                return process_type(type_spec[0])

            return None

        # Complex types defined as dictionaries
        if isinstance(type_spec, dict):
            type_name = type_spec.get("type")

            # Record type (object with fields)
            if type_name == "record":
                return process_record(type_spec)

            # Array type (list)
            elif type_name == "array":
                items = type_spec.get("items")
                # We crate a list with a single element
                return [process_type(items)]

            # Map type (dictionary/object)
            elif type_name == "map":
                values = type_spec.get("values")
                # We create a dictionary with a single key
                return {"key": process_type(values)}

            # If the type is directly primitive
            elif type_name in DEFAULT_PER_TYPE:
                return DEFAULT_PER_TYPE[type_name]

        # If we can't determine the type, we return None
        return None

    # We start processing the schema
    return process_schema(schema)


def generate_test_event_data_for_data_type(data_type: Any) -> dict:  # pragma: no cover
    """
    Generates test data for use in the event bus test cases.

    Builds data by filling in dummy data for basic data types (int/float/bool/str)
    and recursively breaks down the classes for nested classes into basic data types.
    Also supports complex container types like List[dict[str, str]], Dict[str, List[int]],
    List[EventData], and Dict[str, EventData].

    Args:
        data_type (Any): The type of the data which we are generating data for

    Returns:
        dict: A data dictionary containing dummy data for all attributes of the class

    Raises:
        TypeError: If a dictionary has non-string keys (not compatible with AVRO)
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

    # Handle origin types
    origin_type = get_origin(data_type)

    if origin_type is not None:

        args = get_args(data_type)

        # Handle List types
        if origin_type is list:

            item_type = args[0]

            # Handle List of Dicts, e.g. List[Dict[str, str]]
            if get_origin(item_type) is dict:
                dict_key_type, dict_value_type = get_args(item_type)
                # Only support string keys for Avro compatibility
                if dict_key_type is not str:
                    raise TypeError("Avro maps only support string keys. The key type must be 'str'.")

                sample_dict = {}
                if get_origin(dict_value_type) is not None:
                    # Handle nested types in dictionary values, e.g. List[str]
                    sample_dict = {"key": generate_test_event_data_for_data_type(dict_value_type)}
                else:
                    # Handle simple types in dictionary values, e.g. str
                    default_value = defaults_per_type.get(dict_value_type, "default_value")
                    sample_dict = {"key": default_value}

                return [sample_dict]

            # Handle List of simple types, e.g. List[str]
            if item_type in defaults_per_type:
                return [defaults_per_type[item_type]]

            # Handle List of attrs classes, e.g. List[EventData]
            item_data = generate_test_event_data_for_data_type(item_type)
            return [item_data]

        # Handle Dict types
        elif origin_type is dict:

            key_type, value_type = args[0], args[1]

            # Only support string keys for Avro compatibility
            if key_type is not str:
                raise TypeError("Avro maps only support string keys. The key type must be 'str'.")

            # Handle Dict of simple types, e.g. Dict[str, str]
            if value_type in defaults_per_type:
                return {"key": defaults_per_type[value_type]}

            # Handle Dict of List types, e.g. Dict[str, List[int]]
            if get_origin(value_type) is list:
                list_item_type = get_args(value_type)[0]
                return {"key": [defaults_per_type[list_item_type]]}

            # Handle Dict of attrs classes, e.g. Dict[str, EventData]
            value_data = generate_test_event_data_for_data_type(value_type)
            return {"key": value_data}

    # Handle attrs classes
    if hasattr(data_type, "__attrs_attrs__"):

        data_dict = {}

        for attribute in data_type.__attrs_attrs__:

            result = defaults_per_type.get(attribute.type, None)
            # Handle simple types
            if result is not None:
                data_dict.update({attribute.name: result})
            else:
                # Handle origin types in attributes
                origin = get_origin(attribute.type)
                if origin is not None:
                    data_dict.update({attribute.name: generate_test_event_data_for_data_type(attribute.type)})
                # Handle attrs classes
                if hasattr(attribute.type, "__attrs_attrs__"):
                    attr_data = generate_test_event_data_for_data_type(attribute.type)
                    data_dict.update({attribute.name: attr_data})

        return data_type(**data_dict)


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
        example_data_processed = generate_test_event_data_for_data_type(curr_class)
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

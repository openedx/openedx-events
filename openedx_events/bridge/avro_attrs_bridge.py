"""
Code to convert attr classes to Avro specification.

TODO (EventBus): handle optional parameters and allow for schema evolution (ARCHBOM-2013)
"""
import json
from typing import Any, Dict

import attr
import fastavro

from openedx_events.bridge.avro_attrs_bridge_extensions import (
    CourseKeyAvroAttrsBridgeExtension,
    DatetimeAvroAttrsBridgeExtension,
)
from openedx_events.bridge.avro_types import PYTHON_TYPE_TO_AVRO_MAPPING


class AvroAttrsBridge:
    """
    Convert between Avro and OpenEdxPublicSignal data specifications.

    Intended use: To abstract serialization and deserialization of openedx-events to send over an event bus
    The bridge can be used to both automatically generate an Avro schema for the events sent by the associated
    signal instance and to serialize the events themselves using the generated schema.
    TODO (EventBus): rename this class and file to convey that the bridge now works with entire signal
    definitions rather than just attrs classes (ARCHBOM-2101)
    """

    # default extensions, can be overwritten by passing in extensions during obj initialization
    default_extensions = {
        DatetimeAvroAttrsBridgeExtension.cls: DatetimeAvroAttrsBridgeExtension(),
        CourseKeyAvroAttrsBridgeExtension.cls: CourseKeyAvroAttrsBridgeExtension(),
    }

    def __init__(self, signal, extensions=None):
        """
        Init method for Avro Attrs Bridge.

        Arguments:
            signal: An instance of OpenEdxPublicSignal
            extensions: dict mapping a Class to an instance of the required AvroAttrsBridgeExtension subclass, eg
                       { MyDataClass : MyDataClassAvroAttrsBridgeExtension() }
        """
        self.extensions = {}
        self.extensions.update(self.default_extensions)
        if isinstance(extensions, dict):
            self.extensions.update(extensions)

        self._signal = signal
        # Used by _create_avro_field_definition function to keep track of which
        # records have already been defined in schema.
        # Reason: fastavro does not allow you to define record with same name twice
        self.schema_record_names = set()
        self.schema_dict = self._avro_schema_dict_from_signal()

        # make sure the schema is parsable
        fastavro.parse_schema(self.schema_dict)

    def schema_str(self):
        """Json dumps schema dict into a string."""
        return json.dumps(self.schema_dict, sort_keys=True)

    def _avro_schema_dict_from_signal(self):
        """
        Generate the Avro schema for events sent by self._signal.

        TODO (EventBus): Include required CloudEvent fields with sensible defaults
        Returns:
            complex dict that defines Avro schema for events sent by self._signal
        """
        base_schema = {
            "name": "CloudEvent",
            "type": "record",
            "doc": "Avro Event Format for CloudEvents created with openedx_events/avro_attrs_bridge",
            "fields": [],
        }

        for data_key, data_type in self._signal.init_data.items():
            base_schema["fields"].append(self._create_avro_field_definition(data_key, data_type))
        return base_schema

    def _create_avro_field_definition(self, data_key, data_type):
        """
        Create an Avro schema field definition from an OpenEdxPublicSignal data definition.

        Arguments:
            data_key: Field name
            data_type: Python data type, eg `str`, `CourseKey`, `CourseEnrollmentData`
        """
        # Case 1: data_type has known extension
        if extension := self.extensions.get(data_type, None):
            return {
                "name": data_key,
                "type": extension.record_fields(),
            }
        # Case 2: data_type is a simple type that can be converted directly to an Avro type
        elif data_type in PYTHON_TYPE_TO_AVRO_MAPPING:
            if PYTHON_TYPE_TO_AVRO_MAPPING[data_type] in ["record", "array"]:
                # TODO (EventBus): figure out how to handle container types (dicts and arrays). (ARCHBOM-2095)
                raise Exception("Unable to generate Avro schema for dict or array fields")
            return {
                "name": data_key,
                "type": PYTHON_TYPE_TO_AVRO_MAPPING[data_type],
            }

        # Case 2: data_type is an attrs class
        elif hasattr(data_type, "__attrs_attrs__"):
            # Inner Attrs Class

            # fastavro does not allow you to redefine the same record type more than once,
            # so only define an attr record once
            if data_type.__name__ in self.schema_record_names:
                return {
                    "name": data_key,
                    "type": data_type.__name__,
                }
            else:
                self.schema_record_names.add(data_type.__name__)
                return self._generate_avro_record_for_attrs_class(
                    data_type, data_key
                )
        else:
            raise TypeError(
                f"Data type {data_type} is not supported by AvroAttrsBridge. The data type needs to either"
                " be one of the types in PYTHON_TYPE_TO_AVRO_MAPPING, an attrs decorated class, or one of the types"
                " defined in self.extensions."
            )

    def _generate_avro_record_for_attrs_class(
        self, attrs_class, field_name: str
    ) -> Dict[str, Any]:
        """
        Generate Avro record for attrs_class.

        Will also recursively generate Avro records for any sub attr classes and any custom types.

        Custom types are handled by AvroAttrsBridgeExtension subclass instance values defined in self.extensions dict
        """
        field: Dict[str, Any] = {}
        field["name"] = field_name
        field["type"] = dict(name=attrs_class.__name__, type="record", fields=[])

        for attribute in attrs_class.__attrs_attrs__:
            field["type"]["fields"].append(
                self._create_avro_field_definition(attribute.name, attribute.type)
            )
        return field

    def to_dict(self, event_data):
        """
        Convert event_data into dictionary that matches Avro schema (self.schema).

        Warning: this does not validate that the data_dict input matches self._signal

        Arguments:
            event_data: dict with all the values specified in OpenEdxPublicSignal.init_data.
        """
        # TODO (EventBus): is there better way to do this besides using json?
        # This first converts data_dict to json string and then back to dict.

        return json.loads(
            json.dumps(
                event_data, sort_keys=True, default=self._event_value_to_json
            )
        )

    def _event_value_to_json(self, value):
        """
        Serialize a top-level value in an event data dictionary to match the Avro schema.
        """
        # Case 1: Value is an instance of an attrs-decorated class
        if hasattr(value, "__attrs_attrs__"):
            return attr.asdict(value, value_serializer=self._serialize_non_attrs_instance)
        # Case 2: Value is an instance of a class (or subclass) for which the bridge has a known extension
        for extended_class, extension in self.extensions.items():
            if issubclass(type(value), extended_class):
                return extension.serialize(value)
        # Case 3: Default
        return value

    def _serialize_non_attrs_instance(self, _, field, value):
        """
        Use an extension to serialize a value of the appropriate class.

        Used as a callback to attr.asdict to handle any inner fields that are not attrs classes or primitives
        """
        extension = self.extensions.get(field.type, None)
        if extension is not None:
            return extension.serialize(value)
        return value

    def from_dict(self, data: dict):
        """
        Convert dict into event data that can be sent with self._signal.

        Arguments:
            data: Dictionary returned from AvroDeserializer

        Returns:
            dict: Event data dictionary
        """
        return dict([(data_key, self._deserialized_avro_dict_to_object(data[data_key], data_type))
                     for data_key, data_type in self._signal.init_data.items()])

    def _deserialized_avro_dict_to_object(self, data: dict, data_type):
        """
        Convert dictionary entry into an instance of data_type.

        Used to convert messages from an AvroDeserializer into events that can be sent by the
        appropriate signal instance

        Arguments:
            data: Dictionary returned from AvroDeserializer
            data_type: Desired Python data type, eg `str`, `CourseKey`, `CourseEnrollmentData`

        Returns:
            An instance of data_type
        """
        if not hasattr(data_type, '__attrs_attrs__'):
            if extension := self.extensions.get(data_type, None):
                return extension.deserialize(data)
            else:
                raise TypeError(
                    f"Unable to deserialize {data_type} data, please add extension for custom data type"
                )

        for attribute in data_type.__attrs_attrs__:
            if attribute.name in data:
                sub_data = data[attribute.name]
                if sub_data is None:
                    # delete keys that have defaults in attr class and which have None as value
                    # this is to let attr class take care of creating default values
                    if attribute.default is not attr.NOTHING:
                        del data[attribute.name]
                else:
                    if hasattr(attribute.type, "__attrs_attrs__"):
                        if attribute.name in data:
                            data[attribute.name] = self._deserialized_avro_dict_to_object(
                                sub_data, attribute.type
                            )
                    elif attribute.type in self.extensions:
                        extension = self.extensions.get(attribute.type)
                        if attribute.name in data:
                            data[attribute.name] = extension.deserialize(sub_data)
                        else:
                            raise Exception(
                                f"Necessary key: {attribute.name} not found in data dict"
                            )
                    elif attribute.type not in PYTHON_TYPE_TO_AVRO_MAPPING:
                        raise TypeError(
                            f"Unable to deserialize {attribute.type} data, please add extension for custom data type"
                        )

        return data_type(**data)

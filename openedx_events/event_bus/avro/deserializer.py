"""
Deserialize Avro record dictionaries to events that can be sent with OpenEdxPublicSignals.
"""
import io
import json
from typing import get_args, get_origin

import attr
import fastavro

from .custom_serializers import DEFAULT_CUSTOM_SERIALIZERS
from .schema import schema_from_signal
from .types import PYTHON_TYPE_TO_AVRO_MAPPING, SIMPLE_PYTHON_TYPE_TO_AVRO_MAPPING

# Dict of class to deserialize methods (e.g. datetime => DatetimeAvroSerializer.deserialize)
DEFAULT_DESERIALIZERS = {serializer.cls: serializer.deserialize for serializer in DEFAULT_CUSTOM_SERIALIZERS}


def _deserialized_avro_record_dict_to_object(data: dict, data_type, deserializers=None):
    """
    Convert Avro record dictionary into an instance of data_type.

    Used to convert messages from an AvroDeserializer into events that can be sent by the
    appropriate signal instance

    Arguments:
        data: Dictionary representation of an Avro record
        data_type: Desired Python data type, eg `str`, `CourseKey`, `CourseEnrollmentData`
        deserializers: Map of Python data type to deserializer method

    Returns:
        An instance of data_type
    """
    param_deserializers = deserializers or {}
    all_deserializers = {**DEFAULT_DESERIALIZERS, **param_deserializers}
    # get generic type of data_type
    # if data_type == List[int], data_type_origin = list
    data_type_origin = get_origin(data_type)

    if deserializer := all_deserializers.get(data_type, None):
        return deserializer(data)
    elif data_type in PYTHON_TYPE_TO_AVRO_MAPPING:
        return data
    elif data_type_origin == list:
        # Returns types of list contents.
        # Example: if data_type == List[int], arg_data_type = (int,)
        arg_data_type = get_args(data_type)
        if not arg_data_type:
            raise TypeError(
                "List without annotation type is not supported. The argument should be a type, for eg., List[int]"
            )
        # Check whether list items type is in basic types.
        if arg_data_type[0] in SIMPLE_PYTHON_TYPE_TO_AVRO_MAPPING:
            return data
    elif data_type_origin == dict:
        # Returns types of dict contents.
        # Example: if data_type == Dict[str, int], arg_data_type = (str, int)
        arg_data_type = get_args(data_type)
        if not arg_data_type:
            raise TypeError(
                "Dict without annotation type is not supported. The argument should be a type, for eg., Dict[str, int]"
            )
        # Check whether dict items type is in basic types.
        if all(arg in SIMPLE_PYTHON_TYPE_TO_AVRO_MAPPING for arg in arg_data_type):
            return data
    elif hasattr(data_type, "__attrs_attrs__"):
        transformed = {}
        for attribute in data_type.__attrs_attrs__:
            if attribute.name in data:
                sub_data = data[attribute.name]
                if sub_data or attribute.default is attr.NOTHING:
                    transformed[attribute.name] = _deserialized_avro_record_dict_to_object(sub_data,
                                                                                           attribute.type,
                                                                                           deserializers=deserializers)

        return data_type(**transformed)
    raise TypeError(
        f"Unable to deserialize {data_type} data, please add CustomTypeAvroSerializer for custom data type"
    )


def _avro_record_dict_to_event_data(signal, avro_record_dict, deserializers=None):
    """
    Convert an Avro record dictionary into event data that can be sent by the given signal.

    Arguments:
        - signal: An instance of OpenEdxPublicSignal
        - avro_record_dict: Dictionary representation of an Avro record
        - deserializers: Map of Python data type to deserializer method

    Returns:
        - An event data dictionary that can be sent by the given signal
    """
    return {data_key: _deserialized_avro_record_dict_to_object(avro_record_dict[data_key], data_type, deserializers)
            for data_key, data_type in signal.init_data.items()}


def deserialize_bytes_to_event_data(bytes_from_wire, signal):
    """
    Deserialize event_bus and Avro-serialized data.

    Arguments:
        bytes_from_wire: data that was serialized by an Avro serializer
        signal: An instance of OpenEdxPublicSignal
    """
    deserializer = AvroSignalDeserializer(signal)
    schema_dict = deserializer.schema
    data_file = io.BytesIO(bytes_from_wire)
    as_dict = fastavro.schemaless_reader(data_file, schema_dict)
    return deserializer.from_dict(as_dict)


class AvroSignalDeserializer:
    """
    Class to deserialize Avro records into events that can be sent by self.signal.

    The ``schema_string`` and ``from_dict`` methods are the API for this deserializer. This API is derived from the
    confluent_kafka.AvroDeserializer class, which is part of the Kafka event bus ecosystem. The AvroDeserializer takes a
    schema (as string) and a from_dict method as initialization parameters. These methods could also potentially be used
    by other event bus implementations.

    To deserialize events that include data types that are not yet supported, see README.
    """

    def __init__(self, signal):
        """
        Initialize deserializer, creating an Avro schema from signal.

        Arguments:
            signal: An instance of OpenEdxPublicSignal.
        """
        self.signal = signal
        self.deserializers = {ext.cls: ext.deserialize for ext in self.custom_type_serializers()}
        self.custom_types = {ext.cls: ext.field_type for ext in self.custom_type_serializers()}
        self.schema = schema_from_signal(self.signal, custom_type_to_avro_type=self.custom_types)

    def schema_string(self):
        """Get Avro schema as string."""
        return json.dumps(self.schema, sort_keys=True)

    def from_dict(self, avro_record_dict):
        """Convert Avro record dictionary to event data."""
        return _avro_record_dict_to_event_data(self.signal, avro_record_dict, self.deserializers)

    def custom_type_serializers(self):
        """
        Override this method to add custom serializers for unhandled classes.

        Returns:
            - A list of subclasses of BaseCustomTypeAvroSerializer
        """
        return []

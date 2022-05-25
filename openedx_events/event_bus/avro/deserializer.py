"""
Deserialize Avro records to events that can be sent with OpenEdxPublicSignals.
"""
import json
from datetime import datetime

import attr
from opaque_keys.edx.keys import CourseKey

from .custom_serializers import CourseKeyAvroSerializer, DatetimeAvroSerializer
from .schema import schema_from_signal
from .types import PYTHON_TYPE_TO_AVRO_MAPPING

DEFAULT_DESERIALIZERS = {
    datetime: DatetimeAvroSerializer.deserialize,
    CourseKey: CourseKeyAvroSerializer.deserialize,
}


def _deserialized_avro_dict_to_object(data: dict, data_type, deserializers=None):
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
    param_deserializers = deserializers or {}
    all_deserializers = {**DEFAULT_DESERIALIZERS, **param_deserializers}

    if deserializer := all_deserializers.get(data_type, None):
        return deserializer(data)
    elif data_type in PYTHON_TYPE_TO_AVRO_MAPPING:
        return data
    elif hasattr(data_type, "__attrs_attrs__"):
        transformed = {}
        for attribute in data_type.__attrs_attrs__:
            if attribute.name in data:
                sub_data = data[attribute.name]
                if sub_data or attribute.default is attr.NOTHING:
                    transformed[attribute.name] = _deserialized_avro_dict_to_object(sub_data,
                                                                                    attribute.type,
                                                                                    deserializers=deserializers)

        return data_type(**transformed)
    raise TypeError(
        f"Unable to deserialize {data_type} data, please add extension for custom data type"
    )


def _record_dict_to_event_data(signal, avro_record, deserializers=None):
    return {data_key: _deserialized_avro_dict_to_object(avro_record[data_key], data_type, deserializers)
            for data_key, data_type in signal.init_data.items()}


class AvroSignalDeserializer:
    """
    Class to deserialize Avro records into events that can be sent by self.signal.

    The schema_string and from_dict methods can be used by the confluent_kafka.AvroDeserializer class when creating
    an event consumer.
    To deserialize events with non-attrs, non-primitive data types, override this class by including the appropriate
    BaseCustomTypeAvroSerializer subclasses.
    """

    def __init__(self, signal):
        """Initialize schema with signal."""
        self.signal = signal
        self.deserializers = {ext.cls: ext.deserialize for ext in self.custom_type_serializers()}
        self.custom_types = {ext.cls: ext.field_type for ext in self.custom_type_serializers()}
        self.schema = schema_from_signal(self.signal, custom_field_types=self.custom_types)

    def schema_string(self):
        """Get Avro schema as string."""
        return json.dumps(self.schema, sort_keys=True)

    def from_dict(self, record_dict):
        """Convert Avro record dictionary to event data."""
        return _record_dict_to_event_data(self.signal, record_dict, self.deserializers)

    def custom_type_serializers(self):
        """Override this method to add custom serializers for non-attrs, non-primitive classes."""
        return []

"""
Serialize events to Avro records.
"""
import json
from datetime import datetime

import attr
from opaque_keys.edx.keys import CourseKey

from .custom_serializers import CourseKeyAvroSerializer, DatetimeAvroSerializer
from .schema import schema_from_signal

DEFAULT_SERIALIZERS = {
    datetime: DatetimeAvroSerializer.serialize,
    CourseKey: CourseKeyAvroSerializer.serialize,
}


def _get_non_attrs_serializer(serializers=None):
    """Create a method to pass to attr.as_dict that will serialize using custom serializers."""
    param_serializers = serializers or {}
    all_serializers = {**DEFAULT_SERIALIZERS, **param_serializers}

    def _serialize_non_attrs_values(inst, field, value):  # pylint: disable=unused-argument
        for extended_class, serializer in all_serializers.items():
            if field:
                if issubclass(field.type, extended_class):
                    return serializer(value)
            if issubclass(type(value), extended_class):
                return serializer(value)
        return value
    return _serialize_non_attrs_values


def _event_data_to_record_dict(event_data, serializers=None):
    """Create a pure dict (no compound objects) from an event data dict."""

    def value_to_dict(value):
        # Case 1: Value is an instance of an attrs-decorated class
        if hasattr(value, "__attrs_attrs__"):
            return attr.asdict(value, value_serializer=_get_non_attrs_serializer(serializers))
        return _get_non_attrs_serializer(serializers)(None, None, value)

    return json.loads(
        json.dumps(
            event_data, sort_keys=True, default=value_to_dict
        )
    )


class AvroSignalSerializer:
    """
    Class to serialize events into Avro records that can be sent via an event bus.

    The schema_string and to_dict methods can be used by the confluent_kafka.AvroSerializer class when creating
    an event producer.
    To serialize events with non-attrs, non-primitive data types, override this class by including the appropriate
    BaseCustomTypeAvroSerializer subclasses.
    """

    def __init__(self, signal):
        """Create Avro schema using signal."""
        self.signal = signal
        self.serializers = {ext.cls: ext.serialize for ext in self.custom_type_serializers()}
        self.custom_types = {ext.cls: ext.field_type for ext in self.custom_type_serializers()}
        self.schema = schema_from_signal(self.signal, custom_field_types=self.custom_types)

    def schema_string(self):
        """Get Avro schema as JSON string."""
        return json.dumps(self.schema, sort_keys=True)

    def to_dict(self, event_data):
        """Convert event data to an Avro record (dictionary)."""
        return _event_data_to_record_dict(event_data, serializers=self.serializers)

    def custom_type_serializers(self):
        """Override this method to add custom serializers for non-attrs, non-primitive classes."""
        return []

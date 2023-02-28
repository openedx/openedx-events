"""
Serialize events to Avro records.
"""
import io
import json

import attr
import fastavro

from .custom_serializers import DEFAULT_CUSTOM_SERIALIZERS
from .schema import schema_from_signal

DEFAULT_SERIALIZERS = {serializer.cls: serializer.serialize for serializer in DEFAULT_CUSTOM_SERIALIZERS}


def _get_non_attrs_serializer(serializers=None):
    """
    Create a method to pass as the value_serializer argument to attr.as_dict to serialize using custom serializers.

    Arguments:
        serializers: A map of Python type to serialization method

    Returns:
        A method for serializing non_attrs values
    """
    param_serializers = serializers or {}
    all_serializers = {**DEFAULT_SERIALIZERS, **param_serializers}

    def _serialize_non_attrs_values(inst, field, value):  # pylint: disable=unused-argument
        if value is None:
            # All default=None fields are implicit union types of NoneType
            # and something else. (See ADR 7.) Note that if there isn't a
            # default at all, field.default will be attrs.NOTHING, not None.
            if field.default is None:
                return None
            else:
                # Bail out early with an informative message rather
                # than ending up with an inscrutable error from inside
                # a custom serializer.
                #
                # If we ever make a custom serializer that can handle
                # None as an input, we can remove this check.
                # pylint: disable-next=broad-exception-raised
                raise Exception("None cannot be handled by custom serializers (and default=None was not set)")

        for extended_class, serializer in all_serializers.items():
            if field:
                # Make sure that field.type is a class first.
                if isinstance(field.type, type) and issubclass(field.type, extended_class):
                    return serializer(value)
            if issubclass(type(value), extended_class):
                return serializer(value)
        return value
    return _serialize_non_attrs_values


def _event_data_to_avro_record_dict(event_data, serializers=None):
    """
    Create an Avro record dictionary from an event data dict.

    Arguments:
        event_data: A dictionary representing an event sent by an instance of OpenEdxPublicSignal
        serializers: A map of Python type to serialization method

    Returns:
        An Avro record dictionary representation of the event data
    """

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


def serialize_event_data_to_bytes(event_data, signal):
    """
    Serialize event data to bytes.

    Arguments:
        event_data: Event data to be sent via an OpenEdxPublicSignal's send_event method
        signal: An instance of OpenEdxPublicSignal
    Returns:
        bytes: Byte representation of the event_data, to be sent over the wire
    """
    serializer = AvroSignalSerializer(signal)
    schema_dict = serializer.schema
    out = io.BytesIO()
    data_dict = serializer.to_dict(event_data)
    fastavro.schemaless_writer(out, schema_dict, data_dict)
    out.seek(0)
    return out.read()


class AvroSignalSerializer:
    """
    Class to serialize event data dictionaries into Avro record dictionaries that can be sent by an event bus.

    The ``schema_string`` and ``to_dict`` methods are the API for this deserializer. This API is derived from the
    confluent_kafka.AvroSerializer class, which is part of the Kafka event bus ecosystem. The AvroSerializer takes a
    schema (as string) and a to_dict method as initialization parameters. These methods could also potentially be used
    by other event bus implementations.

    To serialize events that include data types that are not yet supported, see README.
    """

    def __init__(self, signal):
        """
        Initialize serializer, creating an Avro schema from signal.

        Arguments:
            signal: An instance of OpenEdxPublicSignal
        """
        self.signal = signal
        self.serializers = {ext.cls: ext.serialize for ext in self.custom_type_serializers()}
        self.custom_types = {ext.cls: ext.field_type for ext in self.custom_type_serializers()}
        self.schema = schema_from_signal(self.signal, custom_type_to_avro_type=self.custom_types)

    def schema_string(self):
        """Get Avro schema as JSON string."""
        return json.dumps(self.schema, sort_keys=True)

    def to_dict(self, event_data):
        """Convert event data to an Avro record dictionary."""
        return _event_data_to_avro_record_dict(event_data, serializers=self.serializers)

    def custom_type_serializers(self):
        """
        Override this method to add custom serializers for unhandled classes.

        Returns:
            A list of subclasses of BaseCustomTypeAvroSerializer
        """
        return []

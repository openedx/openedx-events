"""
Utility methods and classes for testing various modules in event_bus.avro.
"""
import io
import re

import attr
import fastavro

from openedx_events.event_bus.avro.custom_serializers import BaseCustomTypeAvroSerializer
from openedx_events.event_bus.avro.deserializer import AvroSignalDeserializer
from openedx_events.event_bus.avro.serializer import AvroSignalSerializer
from openedx_events.event_bus.avro.types import PYTHON_TYPE_TO_AVRO_MAPPING
from openedx_events.tooling import OpenEdxPublicSignal


def create_simple_signal(data_dict):
    """
    Create a basic OpenEdxPublicSignal with init_data = data_dict.

    Arguments:
        data_dict: Description of attributes passed to the signal
    """
    return OpenEdxPublicSignal(
        event_type="simple.signal",
        data=data_dict
    )


def serialize_event_data_to_bytes(event_data, signal):
    """
    Utility method to make sure an Avro serializer can actually serialize given a schema and data
    to serialize

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


def deserialize_bytes_to_event_data(bytes_from_wire, signal):
    """
    Utility method to make sure an Avro deserializer can actually deserialize given a event_bus and Avro-serialized
    data

    Arguments:
        bytes_from_wire: data that was serialized by an Avro serializer
        signal: An instance of OpenEdxPublicSignal
    """
    deserializer = AvroSignalDeserializer(signal)
    schema_dict = deserializer.schema
    data_file = io.BytesIO(bytes_from_wire)
    as_dict = fastavro.schemaless_reader(data_file, schema_dict)
    return deserializer.from_dict(as_dict)


# Useful simple attr classes
@attr.s(auto_attribs=True)
class SimpleAttrs:
    """Class with all primitive type fields"""
    boolean_field: bool
    int_field: int
    float_field: float
    bytes_field: bytes
    string_field: str


@attr.s(auto_attribs=True)
class SubTestData0:
    """Subclass for testing nested attrs"""
    sub_name: str
    course_id: str


@attr.s(auto_attribs=True)
class SubTestData1:
    """Subclass for testing nested attrs"""
    sub_name: str
    course_id: str


@attr.s(auto_attribs=True)
class EventData:
    """More complex class for testing nested attrs"""
    sub_name: str
    course_id: str
    sub_test_0: SubTestData0
    sub_test_1: SubTestData1


@attr.s(frozen=True)
class SimpleAttrsWithDefaults:
    """Test attrs with nullable values"""
    boolean_field = attr.ib(type=bool, default=None)
    int_field = attr.ib(type=int, default=None)
    float_field = attr.ib(type=float, default=None)
    bytes_field = attr.ib(type=bytes, default=None)
    string_field = attr.ib(type=str, default=None)
    attrs_field = attr.ib(type=SimpleAttrs, default=None)


@attr.s(frozen=True)
class NestedAttrsWithDefaults:
    """Test attrs with nullable values"""
    field_0 = attr.ib(type=SimpleAttrsWithDefaults)


class NonAttrs:
    """Test data class not decorated with @attr."""
    def __init__(self, val0, val1):
        self.val0 = val0
        self.val1 = val1

    def __eq__(self, other):
        # Treat all instances with the same values as equal for easier testing
        return self.val0 == other.val0 and self.val1 == other.val1


@attr.s(frozen=True)
class NestedNonAttrs:
    """Test attrs with nullable values"""
    field_0 = attr.ib(type=NonAttrs)


class NonAttrsAvroSerializer(BaseCustomTypeAvroSerializer):
    """Custom serializer for Non-Attrs class"""

    cls = NonAttrs
    field_type = PYTHON_TYPE_TO_AVRO_MAPPING[str]

    @staticmethod
    def serialize(obj) -> str:
        return f"{obj.val0}:{obj.val1}"

    @staticmethod
    def deserialize(data: str) -> object:
        bits = re.split(":", data)
        return NonAttrs(bits[0], bits[1])


class SpecialSerializer(AvroSignalSerializer):
    def custom_type_serializers(self):
        return [NonAttrsAvroSerializer]


class SpecialDeserializer(AvroSignalDeserializer):
    def custom_type_serializers(self):
        return [NonAttrsAvroSerializer]

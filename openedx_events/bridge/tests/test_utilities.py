"""
Utility methods and classes for testing AvroAttrsBridge
"""
import io
import re

import attr
import fastavro

from openedx_events.bridge.avro_attrs_bridge_extensions import AvroAttrsBridgeExtention
from openedx_events.tooling import OpenEdxPublicSignal


def create_simple_signal(data_dict):
    """
    Create a basic OpenEdxPublicSignal with init_data = data_dict

    Arguments:
        data_dict: Description of attributes passed to the signal
    """
    return OpenEdxPublicSignal(
        event_type="simple.signal",
        data=data_dict
    )


def serialize_event_data_to_bytes(bridge, event_data):
    """
    Utility method to make sure an Avro serializer can actually serialize given a bridge schema and data
    to serialize

    Arguments:
        bridge: An instance of AvroAttrsBridge
        event_data: Event data to be sent via an OpenEdxPublicSignal's send_event method
    Returns:
        bytes: Byte representation of the event_data, to be sent over the wire
    """
    # Try to serialize using the generated schema.
    out = io.BytesIO()
    data_dict = bridge.to_dict(event_data)
    fastavro.schemaless_writer(out, bridge.schema_dict, data_dict)
    out.seek(0)
    return out.read()


def deserialize_bytes_to_event_data(bridge, bytes_from_wire):
    """
    Utility method to make sure an Avro deserializer can actually deserialize given a bridge and Avro-serialized
    data

    Arguments:
        bridge: an instance of AvroAttrsBridge
        bytes_from_wire: data that was serialized by an Avro serializer
    """
    data_file = io.BytesIO(bytes_from_wire)
    as_dict = fastavro.schemaless_reader(data_file, bridge.schema_dict)
    return bridge.from_dict(as_dict)


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
class TestData:
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


@attr.s(frozen=True)
class NestedAttrsWithDefaults:
    """Test attrs with nullable values"""
    field_0 = attr.ib(type=SimpleAttrsWithDefaults, default=None)


class NonAttrs:
    """Data class not decorated with @attr. For testing bridge extension"""
    def __init__(self, val0, val1):
        self.val0 = val0
        self.val1 = val1

    def __eq__(self, other):
        # Treat all instances with the same values as equal for easier testing
        return self.val0 == other.val0 and self.val1 == other.val1


class SimpleBridgeExtension(AvroAttrsBridgeExtention):
    """
    Simple Bridge Extension for de/serializing
    """

    cls = NonAttrs

    def serialize(self, obj) -> str:
        """Serialize obj into string."""
        return f"{obj.val0}:{obj.val1}"

    def deserialize(self, data: str):
        """Deserialize string into obj."""
        bits = re.split(":", data)
        return NonAttrs(bits[0], bits[1])

    def record_fields(self):
        """Define Avro schema for self.cls."""
        return "string"

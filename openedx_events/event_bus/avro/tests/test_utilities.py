"""
Utility methods and classes for testing various modules in event_bus.avro.
"""

import re
from datetime import datetime
from typing import ClassVar

import attr
import attrs
from opaque_keys.edx.keys import CourseKey

from openedx_events.event_bus.avro.custom_serializers import BaseCustomTypeAvroSerializer
from openedx_events.event_bus.avro.deserializer import AvroSignalDeserializer
from openedx_events.event_bus.avro.serializer import AvroSignalSerializer
from openedx_events.event_bus.avro.types import PYTHON_TYPE_TO_AVRO_MAPPING
from openedx_events.tooling import OpenEdxPublicSignal


def create_simple_signal(data_dict, event_type="simple.signal"):
    """
    Create a basic OpenEdxPublicSignal with init_data = data_dict.

    Arguments:
        data_dict: Description of attributes passed to the signal
        event_type: A custom event type string. Defaults to 'simple.signal'
    """
    return OpenEdxPublicSignal(  # pylint: disable=missing-or-incorrect-annotation
        event_type=event_type, data=data_dict
    )


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
class ComplexAttrs:
    """Class with all complex type fields"""

    list_field: list[int]
    dict_field: dict[str, int]


@attr.s(auto_attribs=True)
class NestedComplexAttrs:
    """Class with nested complex type fields"""

    list_of_attr_field: list[SimpleAttrs]
    dict_of_attr_field: dict[str, SimpleAttrs]
    list_of_dict_field: list[dict[str, int]]
    dict_of_list_field: dict[str, list[int]]


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


@attrs.define(frozen=True)
class SimpleAttrsWithDefaults:
    """Test attrs with nullable values"""

    boolean_field: bool = None  # type: ignore[assignment]
    int_field: int = None  # type: ignore[assignment]
    float_field: float = None  # type: ignore[assignment]
    bytes_field: bytes = None  # type: ignore[assignment]
    string_field: str = None  # type: ignore[assignment]
    attrs_field: SimpleAttrs = None  # type: ignore[assignment]


@attrs.define(frozen=True)
class CustomAttrsWithDefaults:
    """Test attrs with nullable values"""

    coursekey_field: CourseKey = None  # type: ignore[assignment]
    datetime_field: datetime = None  # type: ignore[assignment]


@attrs.define(frozen=True)
class CustomAttrsWithoutDefaults:
    """Test attrs without nullable values"""

    coursekey_field: CourseKey
    datetime_field: datetime


@attrs.define(frozen=True)
class NestedAttrsWithDefaults:
    """Test attrs with nullable values"""

    field_0: SimpleAttrsWithDefaults


class NonAttrs:
    """Test data class not decorated with @attr."""

    def __init__(self, val0, val1):
        self.val0 = val0
        self.val1 = val1

    def __eq__(self, other):
        # Treat all instances with the same values as equal for easier testing
        return self.val0 == other.val0 and self.val1 == other.val1


@attrs.define(frozen=True)
class NestedNonAttrs:
    """Test attrs with nullable values"""

    field_0: NonAttrs


class NonAttrsAvroSerializer(BaseCustomTypeAvroSerializer):
    """Custom serializer for Non-Attrs class"""

    cls: ClassVar[type] = NonAttrs
    field_type: ClassVar[str] = PYTHON_TYPE_TO_AVRO_MAPPING[str]

    @staticmethod
    def serialize(obj: NonAttrs) -> str:
        return f"{obj.val0}:{obj.val1}"

    @staticmethod
    def deserialize(data: str) -> NonAttrs:
        bits = re.split(":", data)
        return NonAttrs(bits[0], bits[1])


class SpecialSerializer(AvroSignalSerializer):
    """AvroSignalSerializer with NonAttrs support."""

    def custom_type_serializers(self):
        return [NonAttrsAvroSerializer]


class SpecialDeserializer(AvroSignalDeserializer):
    """AvroSignalDeserializer with NonAttrs support."""

    def custom_type_serializers(self):
        return [NonAttrsAvroSerializer]

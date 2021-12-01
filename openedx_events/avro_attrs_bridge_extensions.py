"""
Classes to serialize and deserialize custom types used by openedx events
"""
from abc import ABC, abstractmethod
from datetime import datetime

from opaque_keys.edx.keys import CourseKey

from openedx_events.avro_attrs_bridge import AVRO_TYPE_FOR


class AvroAttrsBridgeExtention(ABC):
    """
    Used by openedx_events.avro_attrs_bridge.AvroAttrsBridge class to serialize/deserialize custom types
    """
    cls: type

    def type(self):
        return type(self.cls)

    @abstractmethod
    def serialize(self, obj) -> bytes:
        ...

    @abstractmethod
    def deserialize(self, data: bytes) -> object:
        ...

    @abstractmethod
    def record_fields(self):
        ...


class CourseKeyAvroAttrsBridgeExtension(AvroAttrsBridgeExtention):
    """
    AvroAttrsBrdgeExtension for CourseKey class.
    """
    cls = CourseKey

    def serialize(self, obj) -> bytes:
        return str(obj)

    def deserialize(self, data: bytes):
        return CourseKey.from_string(data)

    def record_fields(self):
        return AVRO_TYPE_FOR[str]


class DatetimeAvroAttrsBridgeExtension(AvroAttrsBridgeExtention):
    """
    AvroAttrsBrdgeExtension for CourseKey class.
    """
    cls = datetime

    def serialize(self, obj) -> bytes:
        return obj.isoformat()

    def deserialize(self, data: bytes):
        return datetime.fromisoformat(data)

    def record_fields(self):
        return AVRO_TYPE_FOR[str]

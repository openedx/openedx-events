"""
Classes to serialize and deserialize custom types used by openedx events.
"""
from abc import ABC, abstractmethod
from datetime import datetime

from opaque_keys.edx.keys import CourseKey

from openedx_events.avro_types import AVRO_TYPE_FOR


class AvroAttrsBridgeExtention(ABC):
    """
    Used by openedx_events.avro_attrs_bridge.AvroAttrsBridge class to serialize/deserialize custom types.
    """

    cls: type

    def type(self):
        """Get type of class this extension serilizer and deserializes."""
        return type(self.cls)

    @abstractmethod
    def serialize(self, obj) -> str:
        """Abstart method to serialize obj into string."""
        ...

    @abstractmethod
    def deserialize(self, data: str) -> object:
        """Abstart method to deserialize string array into obj."""
        ...

    @abstractmethod
    def record_fields(self):
        """
        Abstract method to define avro schema for self.cls.

        This is usually just a AVRO_TYPE_FOR[str]
        """
        ...


class CourseKeyAvroAttrsBridgeExtension(AvroAttrsBridgeExtention):
    """
    AvroAttrsBrdgeExtension for CourseKey class.
    """

    cls = CourseKey

    def serialize(self, obj) -> str:
        """Serialize obj into string."""
        return str(obj)

    def deserialize(self, data: str):
        """Deserialize string array into obj."""
        return CourseKey.from_string(data)

    def record_fields(self):
        """Define avro schema for self.cls."""
        return AVRO_TYPE_FOR[str]


class DatetimeAvroAttrsBridgeExtension(AvroAttrsBridgeExtention):
    """
    AvroAttrsBrdgeExtension for CourseKey class.
    """

    cls = datetime

    def serialize(self, obj) -> str:
        """Serialize obj into string."""
        return obj.isoformat()

    def deserialize(self, data: str):
        """Deserialize string array into obj."""
        return datetime.fromisoformat(data)

    def record_fields(self):
        """Define avro schema for self.cls."""
        return AVRO_TYPE_FOR[str]

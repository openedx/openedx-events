"""
Classes to serialize and deserialize custom types used by openedx events.
"""
from abc import ABC, abstractmethod
from datetime import datetime

from opaque_keys.edx.keys import CourseKey

from openedx_events.bridge.avro_types import PYTHON_TYPE_TO_AVRO_MAPPING


class AvroAttrsBridgeExtention(ABC):
    """
    Used by openedx_events.avro_attrs_bridge.AvroAttrsBridge class to serialize/deserialize custom types.
    """

    cls: type

    def type(self):
        """Get type of class this extension serializer and deserializes."""
        return type(self.cls)

    @abstractmethod
    def serialize(self, obj) -> str:
        """Abstract method to serialize obj into string."""
        ...

    @abstractmethod
    def deserialize(self, data: str) -> object:
        """Abstract method to deserialize string array into obj."""
        ...

    @abstractmethod
    def record_fields(self):
        """
        Abstract method to define Avro schema for self.cls.

        This is usually just a PYTHON_TYPE_TO_AVRO_MAPPING[str]
        """
        ...


class CourseKeyAvroAttrsBridgeExtension(AvroAttrsBridgeExtention):
    """
    AvroAttrsBridgeExtension for CourseKey class.
    """

    cls = CourseKey

    def serialize(self, obj) -> str:
        """Serialize obj into string."""
        return str(obj)

    def deserialize(self, data: str):
        """Deserialize string array into obj."""
        return CourseKey.from_string(data)

    def record_fields(self):
        """Define Avro schema for self.cls."""
        return PYTHON_TYPE_TO_AVRO_MAPPING[str]


class DatetimeAvroAttrsBridgeExtension(AvroAttrsBridgeExtention):
    """
    AvroAttrsBridgeExtension for datetime class.

    Note the choice of an iso-formatted string comes directly from the required CloudEvent <-> Avro mapping
    specified here:
     https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/formats/avro-format.md#21-type-system-mapping
    """

    cls = datetime

    def serialize(self, obj) -> str:
        """Serialize obj into string."""
        return obj.isoformat()

    def deserialize(self, data: str):
        """Deserialize string array into obj."""
        return datetime.fromisoformat(data)

    def record_fields(self):
        """Define Avro schema for self.cls."""
        return PYTHON_TYPE_TO_AVRO_MAPPING[str]

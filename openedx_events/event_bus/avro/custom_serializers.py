
"""
Classes to serialize and deserialize custom types used by openedx events.
"""
from abc import ABC, abstractmethod
from datetime import datetime

from opaque_keys.edx.keys import CourseKey

from openedx_events.event_bus.avro.types import PYTHON_TYPE_TO_AVRO_MAPPING


class BaseCustomTypeAvroSerializer(ABC):
    """
    Used by openedx_events.avro_utilities class to serialize/deserialize custom types.
    """

    cls: type
    field_type: str

    def type(self):
        """Get type of class this extension serializer and deserializes."""
        return type(self.cls)

    @staticmethod
    @abstractmethod
    def serialize(obj) -> str:
        """Abstract method to serialize obj into string."""
        ...

    @staticmethod
    @abstractmethod
    def deserialize(data: str) -> object:
        """Abstract method to deserialize string into obj."""
        ...


class CourseKeyAvroSerializer(BaseCustomTypeAvroSerializer):
    """
    CustomTypeAvroSerializer for CourseKey class.
    """

    cls = CourseKey
    field_type = PYTHON_TYPE_TO_AVRO_MAPPING[str]

    @staticmethod
    def serialize(obj) -> str:
        """Serialize obj into string."""
        return str(obj)

    @staticmethod
    def deserialize(data: str):
        """Deserialize string into obj."""
        return CourseKey.from_string(data)


class DatetimeAvroSerializer(BaseCustomTypeAvroSerializer):
    """
    CustomTypeAvroSerializer for datetime class.

    Note the choice of an iso-formatted string comes directly from the required CloudEvent <-> Avro mapping
    specified here:
    https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/formats/avro-format.md#21-type-system-mapping
    """

    cls = datetime
    field_type = PYTHON_TYPE_TO_AVRO_MAPPING[str]

    @staticmethod
    def serialize(obj) -> str:
        """Serialize obj into string."""
        return obj.isoformat()

    @staticmethod
    def deserialize(data: str):
        """Deserialize string into obj."""
        return datetime.fromisoformat(data)

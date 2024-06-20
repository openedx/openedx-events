
"""
Classes to serialize and deserialize custom types used by openedx events. See README for usage.
"""
from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from ccx_keys.locator import CCXLocator
from opaque_keys.edx.keys import CourseKey, UsageKey
from opaque_keys.edx.locator import LibraryLocatorV2, LibraryUsageLocatorV2

from openedx_events.event_bus.avro.types import PYTHON_TYPE_TO_AVRO_MAPPING


class BaseCustomTypeAvroSerializer(ABC):
    """
    Used by openedx_events.avro_utilities class to serialize/deserialize custom types.
    """

    cls: type
    field_type: str

    @staticmethod
    @abstractmethod
    def serialize(obj) -> str:
        """Abstract method to serialize obj into string."""

    @staticmethod
    @abstractmethod
    def deserialize(data: str) -> object:
        """Abstract method to deserialize string into obj."""


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


class CcxCourseLocatorAvroSerializer(BaseCustomTypeAvroSerializer):
    """
    CustomTypeAvroSerializer for CCXLocator class.
    """

    cls = CCXLocator
    field_type = PYTHON_TYPE_TO_AVRO_MAPPING[str]

    @staticmethod
    def serialize(obj) -> str:
        """Serialize obj into string."""
        return str(obj)

    @staticmethod
    def deserialize(data: str):
        """Deserialize string into obj."""
        return CCXLocator.from_string(data)


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


class UsageKeyAvroSerializer(BaseCustomTypeAvroSerializer):
    """
    CustomTypeAvroSerializer for UsageKey class.
    """

    cls = UsageKey
    field_type = PYTHON_TYPE_TO_AVRO_MAPPING[str]

    @staticmethod
    def serialize(obj) -> str:
        """Serialize obj into string."""
        return str(obj)

    @staticmethod
    def deserialize(data: str):
        """Deserialize string into obj."""
        return UsageKey.from_string(data)


class LibraryLocatorV2AvroSerializer(BaseCustomTypeAvroSerializer):
    """
    CustomTypeAvroSerializer for LibraryLocatorV2 class.
    """

    cls = LibraryLocatorV2
    field_type = PYTHON_TYPE_TO_AVRO_MAPPING[str]

    @staticmethod
    def serialize(obj) -> str:
        """Serialize obj into string."""
        return str(obj)

    @staticmethod
    def deserialize(data: str):
        """Deserialize string into obj."""
        return LibraryLocatorV2.from_string(data)


class LibraryUsageLocatorV2AvroSerializer(BaseCustomTypeAvroSerializer):
    """
    CustomTypeAvroSerializer for LibraryUsageLocatorV2 class.
    """

    cls = LibraryUsageLocatorV2
    field_type = PYTHON_TYPE_TO_AVRO_MAPPING[str]

    @staticmethod
    def serialize(obj) -> str:
        """Serialize obj into string."""
        return str(obj)

    @staticmethod
    def deserialize(data: str):
        """Deserialize string into obj."""
        return LibraryUsageLocatorV2.from_string(data)


class UuidAvroSerializer(BaseCustomTypeAvroSerializer):
    """
    CustomTypeAvroSerializer for the UUID class.

    https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/formats/avro-format.md#21-type-system-mapping
    """

    cls = UUID
    field_type = PYTHON_TYPE_TO_AVRO_MAPPING[str]

    @staticmethod
    def serialize(obj) -> str:
        """Serialize obj into string."""
        return str(obj)

    @staticmethod
    def deserialize(data: str):
        """Deserialize string into obj."""
        return UUID(data)


DEFAULT_CUSTOM_SERIALIZERS = [
    CourseKeyAvroSerializer,
    CcxCourseLocatorAvroSerializer,
    DatetimeAvroSerializer,
    LibraryLocatorV2AvroSerializer,
    LibraryUsageLocatorV2AvroSerializer,
    UsageKeyAvroSerializer,
    UuidAvroSerializer,
]

"""
Classes to serialize and deserialize custom types used by openedx events. See README for usage.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, ClassVar
from uuid import UUID

from ccx_keys.locator import CCXLocator
from opaque_keys.edx.keys import CourseKey, UsageKey
from opaque_keys.edx.locator import (
    LibraryCollectionLocator,
    LibraryContainerLocator,
    LibraryLocatorV2,
    LibraryUsageLocatorV2,
)

from openedx_events.event_bus.avro.types import PYTHON_TYPE_TO_AVRO_MAPPING


class BaseCustomTypeAvroSerializer(ABC):
    """
    Used by openedx_events.avro_utilities class to serialize/deserialize custom types.
    """

    cls: ClassVar[type]
    field_type: ClassVar[str]

    @staticmethod
    @abstractmethod
    def serialize(obj: Any) -> str:
        """Abstract method to serialize obj into string."""

    @staticmethod
    @abstractmethod
    def deserialize(data: str) -> Any:
        """Abstract method to deserialize string into obj."""


class CourseKeyAvroSerializer(BaseCustomTypeAvroSerializer):
    """
    CustomTypeAvroSerializer for CourseKey class.
    """

    cls = CourseKey
    field_type = PYTHON_TYPE_TO_AVRO_MAPPING[str]

    @staticmethod
    def serialize(obj: Any) -> str:
        """Serialize obj into string."""
        return str(obj)

    @staticmethod
    def deserialize(data: str) -> CourseKey:
        """Deserialize string into obj."""
        return CourseKey.from_string(data)


class CcxCourseLocatorAvroSerializer(BaseCustomTypeAvroSerializer):
    """
    CustomTypeAvroSerializer for CCXLocator class.
    """

    cls = CCXLocator
    field_type = PYTHON_TYPE_TO_AVRO_MAPPING[str]

    @staticmethod
    def serialize(obj: Any) -> str:
        """Serialize obj into string."""
        return str(obj)

    @staticmethod
    def deserialize(data: str) -> CCXLocator:
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
    def serialize(obj: Any) -> str:
        """Serialize obj into string."""
        # While obj is assumed to be a datetime object, and isoformat()
        # returns a str, we need to accept Any here so to satisfy mypy
        # we no-op cast it to a str.
        return str(obj.isoformat())

    @staticmethod
    def deserialize(data: str) -> datetime:
        """Deserialize string into obj."""
        return datetime.fromisoformat(data)


class UsageKeyAvroSerializer(BaseCustomTypeAvroSerializer):
    """
    CustomTypeAvroSerializer for UsageKey class.
    """

    cls = UsageKey
    field_type = PYTHON_TYPE_TO_AVRO_MAPPING[str]

    @staticmethod
    def serialize(obj: Any) -> str:
        """Serialize obj into string."""
        return str(obj)

    @staticmethod
    def deserialize(data: str) -> UsageKey:
        """Deserialize string into obj."""
        return UsageKey.from_string(data)


class LibraryCollectionLocatorAvroSerializer(BaseCustomTypeAvroSerializer):
    """
    CustomTypeAvroSerializer for LibraryCollectionLocator class.
    """

    cls = LibraryCollectionLocator
    field_type = PYTHON_TYPE_TO_AVRO_MAPPING[str]

    @staticmethod
    def serialize(obj: Any) -> str:
        """Serialize obj into string."""
        return str(obj)

    @staticmethod
    def deserialize(data: str) -> LibraryCollectionLocator:
        """Deserialize string into obj."""
        return LibraryCollectionLocator.from_string(data)


class LibraryContainerLocatorAvroSerializer(BaseCustomTypeAvroSerializer):
    """
    CustomTypeAvroSerializer for LibraryContainerLocator class.
    """

    cls = LibraryContainerLocator
    field_type = PYTHON_TYPE_TO_AVRO_MAPPING[str]

    @staticmethod
    def serialize(obj: Any) -> str:
        """Serialize obj into string."""
        return str(obj)

    @staticmethod
    def deserialize(data: str) -> LibraryContainerLocator:
        """Deserialize string into obj."""
        return LibraryContainerLocator.from_string(data)


class LibraryLocatorV2AvroSerializer(BaseCustomTypeAvroSerializer):
    """
    CustomTypeAvroSerializer for LibraryLocatorV2 class.
    """

    cls = LibraryLocatorV2
    field_type = PYTHON_TYPE_TO_AVRO_MAPPING[str]

    @staticmethod
    def serialize(obj: Any) -> str:
        """Serialize obj into string."""
        return str(obj)

    @staticmethod
    def deserialize(data: str) -> LibraryLocatorV2:
        """Deserialize string into obj."""
        return LibraryLocatorV2.from_string(data)


class LibraryUsageLocatorV2AvroSerializer(BaseCustomTypeAvroSerializer):
    """
    CustomTypeAvroSerializer for LibraryUsageLocatorV2 class.
    """

    cls = LibraryUsageLocatorV2
    field_type = PYTHON_TYPE_TO_AVRO_MAPPING[str]

    @staticmethod
    def serialize(obj: Any) -> str:
        """Serialize obj into string."""
        return str(obj)

    @staticmethod
    def deserialize(data: str) -> LibraryUsageLocatorV2:
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
    def serialize(obj: Any) -> str:
        """Serialize obj into string."""
        return str(obj)

    @staticmethod
    def deserialize(data: str) -> UUID:
        """Deserialize string into obj."""
        return UUID(data)


DEFAULT_CUSTOM_SERIALIZERS: list[type[BaseCustomTypeAvroSerializer]] = [
    CourseKeyAvroSerializer,
    CcxCourseLocatorAvroSerializer,
    DatetimeAvroSerializer,
    LibraryCollectionLocatorAvroSerializer,
    LibraryContainerLocatorAvroSerializer,
    LibraryLocatorV2AvroSerializer,
    LibraryUsageLocatorV2AvroSerializer,
    UsageKeyAvroSerializer,
    UuidAvroSerializer,
]

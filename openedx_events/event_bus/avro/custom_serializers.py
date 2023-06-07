
"""
Classes to serialize and deserialize custom types used by openedx events. See README for usage.
"""
from abc import ABC, abstractmethod
from datetime import datetime

from opaque_keys.edx.keys import CourseKey, UsageKey

from openedx_events.event_bus.avro.types import PYTHON_TYPE_TO_AVRO_MAPPING


import json

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


class DictionaryAvroSerializer(BaseCustomTypeAvroSerializer):
    """
    CustomTypeAvroSerializer for dictionary class.
    """

    cls = dict
    field_type = PYTHON_TYPE_TO_AVRO_MAPPING[dict]

    @staticmethod
    def serialize(obj) -> str:
        """Serialize obj into str."""
        return obj

    @staticmethod
    def deserialize(data: str):
        """Deserialize dict into obj."""
        return json.loads(data)



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


DEFAULT_CUSTOM_SERIALIZERS = [CourseKeyAvroSerializer, DatetimeAvroSerializer, UsageKeyAvroSerializer, DictionaryAvroSerializer]

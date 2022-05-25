"""
Code to convert attr classes to Avro specification.

TODO (EventBus): handle optional parameters and allow for schema evolution (ARCHBOM-2013)
"""
from datetime import datetime

from opaque_keys.edx.keys import CourseKey

from .custom_serializers import CourseKeyAvroSerializer, DatetimeAvroSerializer
from .types import PYTHON_TYPE_TO_AVRO_MAPPING

DEFAULT_FIELD_TYPES = {
    datetime: DatetimeAvroSerializer.field_type,
    CourseKey: CourseKeyAvroSerializer.field_type,
}


def schema_from_signal(signal, custom_field_types=None):
    """Create an Avro schema for events sent by an instance of OpenEdxPublicSignal."""
    field_types = custom_field_types or {}
    all_custom_field_types = {**DEFAULT_FIELD_TYPES, **field_types}
    schema_record_names = set()

    base_schema = {
        "name": "CloudEvent",
        "type": "record",
        "doc": "Avro Event Format for CloudEvents created with openedx_events/schema",
        "fields": [],
    }

    for data_key, data_type in signal.init_data.items():
        base_schema["fields"].append(_create_avro_field_definition(data_key, data_type,
                                                                   schema_record_names,
                                                                   custom_field_types=all_custom_field_types))
    print(f"base_schema: {base_schema}")
    return base_schema


def _create_avro_field_definition(data_key, data_type, schema_record_names,
                                  custom_field_types=None, default_is_none=False):
    """
    Create an Avro schema field definition from an OpenEdxPublicSignal data definition.

    Arguments:
        data_key: Field name
        data_type: Python data type, eg `str`, `CourseKey`, `CourseEnrollmentData`
        schema_record_names: list of previously-encountered data types
        custom_field_types: map of data type to pre-determined avro field type
        default_is_none: boolean indicating whether this field has 'None' as a default
    """
    field = {"name": data_key}
    all_field_type_overrides = custom_field_types or {}

    # Case 1: data_type has a predetermined avro field representation
    if field_type := all_field_type_overrides.get(data_type, None):
        field["type"] = field_type
    # Case 2: data_type is a simple type that can be converted directly to an Avro type
    elif data_type in PYTHON_TYPE_TO_AVRO_MAPPING:
        if PYTHON_TYPE_TO_AVRO_MAPPING[data_type] in ["record", "array"]:
            # TODO (EventBus): figure out how to handle container types (dicts and arrays). (ARCHBOM-2095)
            raise Exception("Unable to generate Avro schema for dict or array fields")
        avro_type = PYTHON_TYPE_TO_AVRO_MAPPING[data_type]
        field["type"] = avro_type

    # Case 3: data_type is an attrs class
    elif hasattr(data_type, "__attrs_attrs__"):
        # Inner Attrs Class

        # fastavro does not allow you to redefine the same record type more than once,
        # so only define an attr record once
        if data_type.__name__ in schema_record_names:
            field["type"] = data_type.__name__
        else:
            schema_record_names.add(data_type.__name__)
            record_type = dict(name=data_type.__name__, type="record", fields=[])

            for attribute in data_type.__attrs_attrs__:
                record_type["fields"].append(
                    _create_avro_field_definition(attribute.name, attribute.type,
                                                  schema_record_names,
                                                  custom_field_types=all_field_type_overrides,
                                                  default_is_none=attribute.default is None)
                )
            field["type"] = record_type
    else:
        raise TypeError(
            f"Data type {data_type} is not supported by AvroAttrsBridge. The data type needs to either"
            " be one of the types in PYTHON_TYPE_TO_AVRO_MAPPING, an attrs decorated class, or one of the types"
            " defined in self.extensions."
        )
    if default_is_none:
        field["default"] = "null"
        single_type = field["type"]
        field["type"] = ["null", single_type]
    return field

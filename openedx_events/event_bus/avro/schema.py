"""
Code to convert attr classes to Avro specification.

TODO (EventBus): handle optional parameters and allow for schema evolution (ARCHBOM-2013)
"""


from .custom_serializers import DEFAULT_CUSTOM_SERIALIZERS
from .types import PYTHON_TYPE_TO_AVRO_MAPPING

DEFAULT_FIELD_TYPES = {serializer.cls: serializer.field_type for serializer in DEFAULT_CUSTOM_SERIALIZERS}


def schema_from_signal(signal, custom_type_to_avro_type=None):
    """
    Create an Avro schema for events sent by an instance of OpenEdxPublicSignal.

    Arguments:
        signal: An instance of OpenEdxPublicSignal
        custom_type_to_avro_type: A map of Python class to Avro type
    """
    field_types = custom_type_to_avro_type or {}
    all_custom_field_types = {**DEFAULT_FIELD_TYPES, **field_types}
    previously_seen_types = set()

    base_schema = {
        "name": "CloudEvent",
        "type": "record",
        "doc": "Avro Event Format for CloudEvents created with openedx_events/schema",
        "fields": [],
    }

    for data_key, data_type in signal.init_data.items():
        base_schema["fields"].append(_create_avro_field_definition(data_key, data_type,
                                                                   previously_seen_types,
                                                                   custom_type_to_avro_type=all_custom_field_types))
    return base_schema


def _create_avro_field_definition(data_key, data_type, previously_seen_types,
                                  custom_type_to_avro_type=None, default_is_none=False):
    """
    Create an Avro schema field definition from an OpenEdxPublicSignal data definition.

    Arguments:
        data_key: Field name, eg `lms_user_id`, `course_id`, `enrollment_status`
        data_type: Python data type, eg `str`, `CourseKey`, `CourseEnrollmentData`
        previously_seen_types: list of previously-encountered data types
        custom_type_to_avro_type: map of custom data types to a pre-determined avro field type
        default_is_none: boolean indicating whether this field has 'None' as a default
    """
    field = {"name": data_key}
    all_field_type_overrides = custom_type_to_avro_type or {}

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
        if data_type.__name__ in previously_seen_types:
            field["type"] = data_type.__name__
        else:
            previously_seen_types.add(data_type.__name__)
            record_type = dict(name=data_type.__name__, type="record", fields=[])

            for attribute in data_type.__attrs_attrs__:
                record_type["fields"].append(
                    _create_avro_field_definition(attribute.name, attribute.type,
                                                  previously_seen_types,
                                                  custom_type_to_avro_type=all_field_type_overrides,
                                                  default_is_none=attribute.default is None)
                )
            field["type"] = record_type
    else:
        raise TypeError(
            f"Data type {data_type} is not supported. The data type needs to either"
            " be one of the types in PYTHON_TYPE_TO_AVRO_MAPPING, an attrs decorated class, or one of the types"
            " defined in custom_type_to_avro_type."
        )
    if default_is_none:
        field["default"] = "null"
        single_type = field["type"]
        field["type"] = ["null", single_type]
    return field

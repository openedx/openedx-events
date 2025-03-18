"""
Code to convert attr classes to Avro specification.

TODO: Handle optional parameters and allow for schema evolution. https://github.com/edx/edx-arch-experiments/issues/53
"""

from typing import Any, Type, get_args, get_origin

from .custom_serializers import DEFAULT_CUSTOM_SERIALIZERS
from .types import PYTHON_TYPE_TO_AVRO_MAPPING, SIMPLE_PYTHON_TYPE_TO_AVRO_MAPPING

DEFAULT_FIELD_TYPES = {serializer.cls: serializer.field_type for serializer in DEFAULT_CUSTOM_SERIALIZERS}


def schema_from_signal(signal, custom_type_to_avro_type=None):
    """
    Create an Avro schema for events sent by an instance of OpenEdxPublicSignal.

    Arguments:
        - signal: An instance of OpenEdxPublicSignal
        - custom_type_to_avro_type: A map of Python class to Avro type

    Returns:
        - An Avro schema definition for the event.
    """
    field_types = custom_type_to_avro_type or {}
    all_custom_field_types = {**DEFAULT_FIELD_TYPES, **field_types}
    previously_seen_types = set()

    base_schema = {
        "name": "CloudEvent",
        "type": "record",
        "doc": "Avro Event Format for CloudEvents created with openedx_events/schema",
        "fields": [],
        "namespace": signal.event_type,
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
        - data_key: Field name, eg `lms_user_id`, `course_id`, `enrollment_status`.
        - data_type: Python data type, eg `str`, `CourseKey`, `CourseEnrollmentData`.
        - previously_seen_types: list of previously-encountered data types.
        - custom_type_to_avro_type: map of custom data types to a pre-determined avro field type.
        - default_is_none: boolean indicating whether this field has 'None' as a default.

    Returns:
        - An Avro field definition.
    """
    field = {"name": data_key}
    all_field_type_overrides = custom_type_to_avro_type or {}
    # get generic type of data_type
    # if data_type == List[int], data_type_origin = list
    data_type_origin = get_origin(data_type)

    # Case 1: data_type has a predetermined avro field representation
    if field_type := all_field_type_overrides.get(data_type, None):
        field["type"] = field_type
    # Case 2: data_type is a simple type that can be converted directly to an Avro type
    elif data_type in PYTHON_TYPE_TO_AVRO_MAPPING:
        if PYTHON_TYPE_TO_AVRO_MAPPING[data_type] in ["map", "array"]:
            # pylint: disable-next=broad-exception-raised
            raise Exception("Unable to generate Avro schema for dict or array fields without annotation types.")
        avro_type = PYTHON_TYPE_TO_AVRO_MAPPING[data_type]
        field["type"] = avro_type
    # Case 3: data_type is a list (possibly with complex items)
    elif data_type_origin is list:
        item_avro_type = _get_avro_type_for_list_item(
            data_type, previously_seen_types, all_field_type_overrides
        )
        field["type"] = {"type": "array", "items": item_avro_type}
    # Case 4: data_type is a dictionary (possibly with complex values)
    elif data_type_origin is dict:
        item_avro_type = _get_avro_type_for_dict_item(
            data_type, previously_seen_types, all_field_type_overrides
        )
        field["type"] = {"type": "map", "values": item_avro_type}
    # Case 5: data_type is an attrs class
    elif hasattr(data_type, "__attrs_attrs__"):
        # Inner Attrs Class

        # fastavro does not allow you to redefine the same record type more than once,
        # so only define an attr record once
        if data_type.__name__ in previously_seen_types:
            field["type"] = data_type.__name__
        else:
            previously_seen_types.add(data_type.__name__)
            record_type = {"name": data_type.__name__, "type": 'record', "fields": []}

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
        field["default"] = None
        single_type = field["type"]
        field["type"] = ["null", single_type]
    return field


def _get_avro_type_for_dict_item(
    data_type: Type[dict], previously_seen_types: set, type_overrides: dict[Any, str]
) -> str | dict[str, str]:
    """
    Determine the Avro type definition for a dictionary value based on its Python type.

    This function converts Python dictionary value types to their corresponding
    Avro type representations. It supports simple types, complex nested types (like
    dictionaries and lists), and custom classes decorated with attrs.

    Args:
        data_type (Type[dict]): The Python dictionary type with its type annotation
            (e.g., Dict[str, str], Dict[str, int], Dict[str, List[str]])
        previously_seen_types (set): Set of type names that have already been
            processed, used to prevent duplicate record definitions
        type_overrides (dict[Any, str]): Dictionary mapping custom Python types to
            their Avro type representations

    Returns:
        One of the following Avro type representations:
        - A string (e.g., "string", "int", "boolean") for simple types
        - A dictionary with a complex type definition for container types, such as:
          - {"type": "array", "items": <avro_type>} for lists
          - {"type": "map", "values": <avro_type>} for nested dictionaries
          - {"name": "<TypeName>", "type": "record", "fields": [...]} for attrs classes
        - A string with a record name for previously defined record types

    Raises:
        TypeError: If the dictionary has no type annotation, has non-string keys,
            or contains unsupported value types
    """
    # Validate dict has type annotation
    # Example: if data_type == Dict[str, int], arg_data_type = (str, int)
    arg_data_type = get_args(data_type)
    if not arg_data_type:
        raise TypeError(
            "Dict without annotation type is not supported. The argument should be a type, e.g. Dict[str, int]"
        )

    value_type = arg_data_type[1]

    # Case 1: Simple types mapped in SIMPLE_PYTHON_TYPE_TO_AVRO_MAPPING
    avro_type = SIMPLE_PYTHON_TYPE_TO_AVRO_MAPPING.get(value_type)
    if avro_type is not None:
        return avro_type

    # Case 2: Complex types (dict, list, or attrs class)
    if get_origin(value_type) in (dict, list) or hasattr(value_type, "__attrs_attrs__"):
        # Create a temporary field for the value type and extract its type definition
        temp_field = _create_avro_field_definition("temp", value_type, previously_seen_types, type_overrides)
        return temp_field["type"]

    # Case 3: Unannotated containers (raise specific errors)
    if value_type is dict:
        raise TypeError("A Dictionary as a dictionary value should have a type annotation.")
    elif value_type is list:
        raise TypeError("A List as a dictionary value should have a type annotation.")

    # Case 4: Unsupported types
    raise TypeError(f"Type {value_type} is not supported for dict values.")

def _get_avro_type_for_list_item(
    data_type: Type[list], previously_seen_types: set, type_overrides: dict[Any, str]
) -> str | dict[str, str]:
    """
    Determine the Avro type definition for a list item based on its Python type.

    This function handles conversion of various Python types that can be
    contained within a list to their corresponding Avro type representations.
    It supports simple types, complex nested types (like dictionaries and lists),
    and custom classes decorated with attrs.

    Args:
        data_type (Type[list]): The Python list type with its type annotation
            (e.g., List[str], List[int], List[Dict[str, str]], etc.)
        previously_seen_types (set): Set of type names that have already been
            processed, used to prevent duplicate record definitions
        type_overrides (dict[Any, str]): Dictionary mapping custom Python types
            to their Avro type representations

    Returns:
        One of the following Avro type representations:
        - A string (e.g., "string", "long", "boolean") for simple types
        - A dictionary with a complex type definition for container types, such as:
          - {"type": "array", "items": <avro_type>} for lists
          - {"type": "map", "values": <avro_type>} for dictionaries
          - {"name": "<TypeName>", "type": "record", "fields": [...]} for attrs classes
        - A string with a record name for previously defined record types

    Raises:
        TypeError: If the list has no type annotation, contains unsupported
            types, or contains containers (dict, list) without proper type
            annotations
    """
    # Validate list has type annotation
    # Example: if data_type == List[int], arg_data_type = (int,)
    arg_data_type = get_args(data_type)
    if not arg_data_type:
        raise TypeError(
            "List without annotation type is not supported. The argument should be a type, e.g. List[int]"
        )

    item_type = arg_data_type[0]

    # Case 1: Simple types mapped in SIMPLE_PYTHON_TYPE_TO_AVRO_MAPPING
    avro_type = SIMPLE_PYTHON_TYPE_TO_AVRO_MAPPING.get(item_type)
    if avro_type is not None:
        return avro_type

    # Case 2: Complex types (dict, list, or attrs class)
    if get_origin(item_type) in (dict, list) or hasattr(item_type, "__attrs_attrs__"):
        # Create a temporary field for the value type and extract its type definition
        temp_field = _create_avro_field_definition("temp", item_type, previously_seen_types, type_overrides)
        return temp_field["type"]

    # Case 3: Unannotated containers (raise specific errors)
    if item_type is dict:
        raise TypeError("A Dictionary as a list item should have a type annotation.")
    elif item_type is list:
        raise TypeError("A List as a list item should have a type annotation.")

    # Case 4: Unsupported types
    raise TypeError(f"Type {item_type} is not supported for list items.")

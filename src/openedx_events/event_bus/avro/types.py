"""A mapping of python types to the Avro type that we want to use make valid avro schema."""
SIMPLE_PYTHON_TYPE_TO_AVRO_MAPPING = {
    bool: "boolean",
    int: "long",
    float: "double",
    bytes: "bytes",
    str: "string",
}
PYTHON_TYPE_TO_AVRO_MAPPING = {
    **SIMPLE_PYTHON_TYPE_TO_AVRO_MAPPING,
    None: "null",
    dict: "map",
    list: "array",
}

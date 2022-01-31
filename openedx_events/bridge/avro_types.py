"""A mapping of python types to the Avro type that we want to use make valid avro schema."""
PYTHON_TYPE_TO_AVRO_MAPPING = {
    None: "null",
    bool: "boolean",
    int: "long",
    float: "double",
    bytes: "bytes",
    str: "string",
    dict: "record",
    list: "array",
}

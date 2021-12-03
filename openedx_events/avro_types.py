# A mapping of python types to the avro type that we want to use make valid avro schema.
AVRO_TYPE_FOR = {
    None: "null",
    bool: "boolean",
    int: "long",
    float: "double",
    bytes: "bytes",
    str: "string",
    dict: "record",
    list: "array",
}

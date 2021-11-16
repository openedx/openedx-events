"""
To run this script you need to first pip install the following:
    pip install attrs fastavro
"""
from typing import Dict, Any
from collections.abc import Mapping
from abc import ABC, abstractmethod

import attr
from pprint import pprint
import json
import fastavro
import io


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

class AvroAttrsBridgeExtention(ABC):

    def serialize(self, obj) -> bytes:
        NotImplemented

    def deserialize(self, data: bytes) -> object:
        NotImplemented

    def record_fields(self, obj_class, field_name: str = "data"):
        NotImplemented

# Some version of this will let us work with pulsar/kafka and abstract their serialization from the end users.
class AvroAttrsBridge:
    def __init__(self, attrs_cls, extension):
        self._attrs_cls = attrs_cls
        schema_string = self.attrs_to_avro_schema(attrs_cls)
        self._schema = fastavro.parse_schema(schema_string)

    def serialize(self, obj) -> bytes:
        """
        Convert from attrs to a valid avro record.
        """
        # Make an valid avro record from the attrs class. in the future `ID`, and time would be generated, the rest
        # would be defined once and maybe passed into the class at instantiation time?
        # Not sure if it makes sense to keep version info here since the schema registry will actually
        # keep track of versions and the topic can have only one associated schema at a time.
        avro_record = dict(
            id="1",
            type="Test.v1",
            time="uea",
            source="test_attrs",
            sourcehost="enki",
            minorversion=0,
            data=attr.asdict(obj),
        )

        # Try to serialize using the generated schema.
        out = io.BytesIO()
        fastavro.schemaless_writer(out, self._schema, avro_record)
        out.seek(0)
        return out.read()

    def deserialize(self, data: bytes) -> object:
        data_file = io.BytesIO(data)
        record = fastavro.schemaless_reader(data_file, self._schema)
        return self.dict_to_attrs(record["data"], self._attrs_cls)

    def schema(self) -> str:
        return self.attrs_to_avro_schema(self._attrs_cls)

    def record_field_for_attrs_class(
        self, attrs_class, field_name: str = "data"
    ) -> Dict[str, Any]:
        field: Dict[str, Any] = {}
        field["name"] = field_name
        field["type"] = dict(name=attrs_class.__name__, type="record", fields=[])

        for attribute in attrs_class.__attrs_attrs__:
            # Attribute is a simple type.
            if attribute.type in AVRO_TYPE_FOR:
                inner_field = {
                    "name": attribute.name,
                    "type": AVRO_TYPE_FOR[attribute.type],
                }
            # Attribute is another attrs class
            elif hasattr(attribute.type, "__attrs_attrs__"):
                # Inner Attrs Class
                inner_field = self.record_field_for_attrs_class(
                    attribute.type, attribute.name
                )
            else:
                NotImplemented

            field["type"]["fields"].append(inner_field)

        return field

    def attrs_to_avro_schema(self, attrs_cls):
        base_schema = {
            "namespace": "io.cloudevents",
            "type": "record",
            "name": "CloudEvent",
            "version": "1.0",
            "doc": "Avro Event Format for CloudEvents",
            "fields": [
                {"name": "id", "type": "string"},
                {"name": "type", "type": "string"},
                {"name": "specversion", "type": "string", "default": "1.0"},
                {"name": "time", "type": "string"},
                {"name": "source", "type": "string"},
                {"name": "sourcehost", "type": "string"},
                {"name": "minorversion", "type": "int"},
            ],
        }

        record_field = self.record_field_for_attrs_class(attrs_cls)
        base_schema["fields"].append(record_field)
        return base_schema

    def dict_to_attrs(self, data: dict, attrs_cls):
        """
        This function mutates the incoming `data` dict argument that's
        passed in.
        """
        for attribute in attrs_cls.__attrs_attrs__:
            if hasattr(attribute.type, "__attrs_attrs__"):
                if attribute.name in data:
                    sub_attr_data = data[attribute.name]
                    data[attribute.name] = self.dict_to_attrs(
                        sub_attr_data, attribute.type
                    )

        return attrs_cls(**data)

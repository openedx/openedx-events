#!/usr/bin/env python3
import io
import fastavro
import json


import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter, BinaryEncoder, BinaryDecoder

def parse_with_schemas(data, *schemas):
    output = []
    for schema in schemas:
        inner_output = {}
        data_file = io.BytesIO(data)
        # make sure data with old schema can still be read by old schema
        try:
            deserialied_data = fastavro.schemaless_reader(data_file, *schema)
            inner_output['data'] = deserialied_data
        except Exception as exc:
            inner_output['exception'] = exc
        output.append(inner_output)
    return output

def temp_serializer(data, schema):
    out = io.BytesIO()
    fastavro.schemaless_writer(out, schema, data)
    out.seek(0)
    return out.read()


def test_avro_changed_schema_add_value_v1():
    """
    Make sure adding an new optional value works
    """
    datum = {
        "userName": "Martin",
        "interests": ["daydreaming", "hacking"],
    }

    expected_datum = dict()
    expected_datum.update(datum)
    expected_datum['favoriteNumber'] = None
    schema = {
        "type": "record",
        "name": "Person",
        "fields": [
            {"name": "userName", "type": "string"},
            {"name": "interests", "type": {"type": "array", "items": "string"}},
        ],
    }

    schema_v2 = {
        "type": "record",
        "name": "Person",
        "fields": [
            {"name": "userName", "type": "string"},
            {"name": "favoriteNumber", "type": ["null","string"], "default": None},
            {"name": "interests", "type": {"type": "array", "items": "string"}},
        ],
    }
    parsed_schema = fastavro.parse_schema(schema)
    parsed_schema_v2 = fastavro.parse_schema(schema_v2)

    serialized_data = temp_serializer(datum, parsed_schema)

    output = parse_with_schemas(serialized_data,(parsed_schema, parsed_schema), (parsed_schema, parsed_schema_v2))
    assert datum == output[0]['data']
    assert output[1]['data'] == expected_datum


def test_avro_changed_schema_add_value_v2():
    """
    Make sure adding an new optional value works
    """
    datum = {
        "userName": "Martin",
        "interests": ["daydreaming", "hacking"],
    }

    expected_datum = dict()
    expected_datum.update(datum)
    expected_datum['favoriteNumber'] = None
    schema = {
        "type": "record",
        "name": "Person",
        "fields": [
            {"name": "userName", "type": "string"},
            {"name": "interests", "type": {"type": "array", "items": "string"}},
        ],
    }

    schema_v2 = {
        "type": "record",
        "name": "Person",
        "fields": [
            {"name": "userName", "type": "string"},
            {"name": "favoriteNumber", "type": ["string","null"], "default": None},
            {"name": "interests", "type": {"type": "array", "items": "string"}},
        ],
    }
    parsed_schema = fastavro.parse_schema(schema)
    parsed_schema_v2 = fastavro.parse_schema(schema_v2)

    serialized_data = temp_serializer(datum, parsed_schema)

    output = parse_with_schemas(serialized_data,(parsed_schema, parsed_schema), (parsed_schema, parsed_schema_v2))
    assert datum == output[0]['data']
    assert output[1]['data'] == expected_datum

def test_avro_changed_schema_remove_value():
    datum = {
        "userName": "Martin",
        "favoriteNumber": "removed_val",
        "interests": ["daydreaming", "hacking"],
    }

    expected_datum = dict()
    expected_datum.update(datum)
    del expected_datum['favoriteNumber']
    schema = {
        "type": "record",
        "name": "Person",
        "fields": [
            {"name": "userName", "type": "string"},
            {"name": "favoriteNumber", "type": "string"},
            {"name": "interests", "type": {"type": "array", "items": "string"}},
        ],
    }

    schema_v2 = {
        "type": "record",
        "name": "Person",
        "fields": [
            {"name": "userName", "type": "string"},
            {"name": "interests", "type": {"type": "array", "items": "string"}},
        ],
    }

    parsed_schema = fastavro.parse_schema(schema)
    parsed_schema_v2 = fastavro.parse_schema(schema_v2)
    serialized_data = temp_serializer(datum, parsed_schema)

    output = parse_with_schemas(serialized_data,(parsed_schema, parsed_schema), (parsed_schema, parsed_schema_v2))
    assert datum == output[0]['data']
    assert output[1]['data'] == expected_datum



def test_avro_changed_schema_missing_val():
    datum = {
        "userName": "Martin",
        "interests": ["daydreaming", "hacking"],
    }

    expected_datum = dict()
    expected_datum.update(datum)
    expected_datum['favoriteNumber'] = None
    schema = {
        "type": "record",
        "name": "Person",
        "fields": [
            {"name": "userName", "type": "string"},
            {"name": "favoriteNumber", "type": ["null","string"], "default":None},
            {"name": "interests", "type": {"type": "array", "items": "string"}},
        ],
    }

    schema_v2 = {
        "type": "record",
        "name": "Person",
        "fields": [
            {"name": "userName", "type": "string"},
            {"name": "interests", "type": {"type": "array", "items": "string"}},
        ],
    }

    parsed_schema = fastavro.parse_schema(schema)
    parsed_schema_v2 = fastavro.parse_schema(schema_v2)
    serialized_data = temp_serializer(datum, parsed_schema)

    output = parse_with_schemas(serialized_data,(parsed_schema, parsed_schema), (parsed_schema, parsed_schema_v2))
    assert expected_datum == output[0]['data']
    assert output[1]['data'] == datum

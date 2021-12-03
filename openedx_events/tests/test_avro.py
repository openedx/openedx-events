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
        inner_output['schema'] = schema
        data_file = io.BytesIO(data)
        # make sure data with old schema can still be read by old schema
        try:
            deserialied_data = fastavro.schemaless_reader(data_file, schema)
            inner_output['data'] = deserialied_data
        except Exception as exc:
            inner_output['exception'] = exc
        output.append(inner_output)
    return output

def parse_with_schemas_avro(data, *schemas):
    output = []
    for schema in schemas:
        inner_output = {}
        inner_output['schema'] = schema
        data_file = io.BytesIO(data)
        # make sure data with old schema can still be read by old schema
        deserialied_data =DatumReader(schema).read(BinaryDecoder(data_file))
        inner_output['data'] = deserialied_data
        output.append(inner_output)
    return output

def temp_serializer_fastavro(data, schema):
    out = io.BytesIO()
    fastavro.schemaless_writer(out, schema, data)
    out.seek(0)
    return out.read()

def temp_serializer_avro(data, schema):
    writer = DatumWriter(schema)
    out = io.BytesIO()
    writer.write(data, BinaryEncoder(out))
    out.seek(0)
    return out.read()

def create_schema_fastavro(schema):
    return fastavro.parse_schema(schema)

def create_schema_avro(schema):
    return avro.schema.parse(json.dumps(schema))



# TODO Create parse_with_schemas for python avro


def test_avro_changed_schema_add_value():
    datum = {
        "userName": "Martin",
        "interests": ["daydreaming", "hacking"],
    }

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
            {"name": "favouriteNumber", "type": ["string", "null"], "default":"default"},
            {"name": "interests", "type": {"type": "array", "items": "string"}},
        ],
    }
    parsed_schema = create_schema_avro(schema)
    parsed_schema_v2 = create_schema_avro(schema_v2)

    serialized_data = temp_serializer_avro(datum, parsed_schema)

    output = parse_with_schemas_avro(serialized_data, parsed_schema, parsed_schema_v2)
    assert datum == output[0]['data']
    # TODO Figure out what is happening
    # data_file = io.BytesIO(serialized_data)
    # # make sure data with old schema can still be read by old schema
    # assert datum == fastavro.schemaless_reader(data_file, parsed_schema)

    # data_file = io.BytesIO(serialized_data)
    # # check to see if data from old schema can be read by new schema
    # record = fastavro.schemaless_reader(data_file, parsed_schema_v2)


def test_avro_changed_schema_remove_value():
    datum = {
        "userName": "Martin",
        "favouriteNumber": "removed_val",
        "interests": ["daydreaming", "hacking"],
    }

    schema = {
        "type": "record",
        "name": "Person",
        "fields": [
            {"name": "userName", "type": "string"},
            {"name": "favouriteNumber", "type": ["null", "string"]},
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

    out = io.BytesIO()
    fastavro.schemaless_writer(out, schema, datum)
    out.seek(0)
    serialized_data = out.read()

    data_file = io.BytesIO(serialized_data)
    # make sure data with old schema can still be read by old schema
    assert datum == fastavro.schemaless_reader(data_file, parsed_schema)

    data_file = io.BytesIO(serialized_data)
    record = fastavro.schemaless_reader(data_file, parsed_schema_v2)
    string_record = json.dumps(record)
    assert "removed_val" not in string_record



def test_avro_changed_schema_missing_val():
    datum = {
        "userName": "Martin",
        "interests": ["daydreaming", "hacking"],
    }

    schema = {
        "type": "record",
        "name": "Person",
        "fields": [
            {"name": "userName", "type": "string"},
            {"name": "favouriteNumber", "type": ["string", "null"], "default": "default"},
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

    out = io.BytesIO()
    fastavro.schemaless_writer(out, parsed_schema, datum)
    out.seek(0)
    serialized_data = out.read()

    data_file = io.BytesIO(serialized_data)
    # make sure data with old schema can still be read by old schema
    read_record = fastavro.schemaless_reader(data_file, parsed_schema)

    data_file = io.BytesIO(serialized_data)
    record = fastavro.schemaless_reader(data_file, parsed_schema_v2)

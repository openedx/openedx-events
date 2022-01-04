"""
Code to convert attr classes to avro specification.
"""
import io
from typing import Dict, Any

import attr
import fastavro
import json
from datetime import datetime
import uuid


from openedx_events.avro_attrs_bridge_extensions import DatetimeAvroAttrsBridgeExtension
from openedx_events.avro_types import AVRO_TYPE_FOR


class AvroAttrsBridge:
    """
    Use to covert between Avro and Attrs data specifications.

    Intended usecase: To abstract serilalization and deserialization of openedx-events to send over pulsar or kafka
    """

    # default extensions, can be overwriteen by passing in extensions during obj initialization
    default_extensions = {
        DatetimeAvroAttrsBridgeExtension.cls: DatetimeAvroAttrsBridgeExtension()
    }
    default_config = {
        "source": "/openedx/unknown/avro_attrs_bridge",
        "sourcehost": "unknown",
        "type": "org.openedx.test.test.test.v0",
    }

    def __init__(self, attrs_cls, extensions=None, config=None):
        """
        Init method for Avro Attrs Bridge

        Arguments:
            attrs_cls: Attr Class Object (not instance)
            extensions: dict mapping Class Object to its AvroAttrsBridgeExtention subclass instance
        """
        self._attrs_cls = attrs_cls

        self.extensions = {}
        self.extensions.update(self.default_extensions)
        if isinstance(extensions, dict):
            self.extensions.update(extensions)

        self.config = {}
        self.config.update(self.default_config)
        if isinstance(config, dict):
            self.config.update(config)

        # used by record_field_for_attrs_class function to track of which records have already been defined in schema
        # Reason: fastavro does no allow you to define record with same name twice
        self.schema_record_names = set()
        self._schema_dict = self.attrs_to_avro_schema(attrs_cls)
        # make sure the schema is parsable
        fastavro.parse_schema(self._schema_dict)

    def schema(self):
        return json.dumps(self._schema_dict, sort_keys=True)

    def attrs_to_avro_schema(self, attrs_cls):
        """
        Generate avro schema for attr_cls

        Arguments:
            attrs_cls: Attr class object
        Returns:
            complex dict tha deines avro schema for attrs_cls
        """
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

        record_fields = self.record_fields_for_attrs_class(attrs_cls)
        base_schema["fields"].append(record_fields)
        return base_schema

    def record_fields_for_attrs_class(
        self, attrs_class, field_name: str = "data"
    ) -> Dict[str, Any]:
        """
        Generate avro record for attrs_class.

        Will also recursively generate avro records for any sub attr classes and any custom types.

        Custom types are handled by AvroAttrsBridgeExtention subclass instance values defined in self.extensions dict
        """
        field: Dict[str, Any] = {}
        field["name"] = field_name
        field["type"] = dict(name=attrs_class.__name__, type="record", fields=[])

        for attribute in attrs_class.__attrs_attrs__:
            # if attribute.name == 'course_key':
            # breakpoint()
            # Attribute is a simple type.
            if attribute.type in AVRO_TYPE_FOR:
                inner_field = {
                    "name": attribute.name,
                    "type": AVRO_TYPE_FOR[attribute.type],
                }

            # Attribute is another attrs class
            elif hasattr(attribute.type, "__attrs_attrs__"):
                # Inner Attrs Class

                # fastavro does not allow you to redefine the same record type more than once,
                # so only define an attr record once
                if attribute.type.__name__ in self.schema_record_names:
                    inner_field = {
                        "name": attribute.name,
                        "type": attribute.type.__name__,
                    }
                else:
                    self.schema_record_names.add(attribute.type.__name__)
                    inner_field = self.record_fields_for_attrs_class(
                        attribute.type, attribute.name
                    )
            else:
                inner_field = None
                extension = self.extensions.get(attribute.type)
                if extension is not None:
                    inner_field = {
                        "name": attribute.name,
                        "type": extension.record_fields(),
                    }
                else:
                    raise TypeError(
                        f"AvroAttrsBridgeExtension for {attribute.type} not in self.extensions."
                    )
            # Assume attribute is optional if it has a default value
            # The default value is always set to None to allow attr class to handle dealing with default values
            # in dict_to_attrs function in this class
            if attribute.default is not attr.NOTHING:
                inner_field["type"] = ["null", inner_field["type"]]
                inner_field["default"] = None
            field["type"]["fields"].append(inner_field)

        return field

    def to_dict(self, obj, context=None):
        """
        TODO: document
        """
        # Make an valid avro record from the attrs class. in the future `ID`, and time would be generated, the rest
        # would be defined once and maybe passed into the class at instantiation time?
        # Not sure if it makes sense to keep version info here since the schema registry will actually
        # keep track of versions and the topic can have only one associated schema at a time.
        obj_as_dict = attr.asdict(obj, value_serializer=self.extension_serializer)
        # TODO what should the default values of the following be
        avro_record = dict(
            id=context["id"]
            if isinstance(context, dict) and "id" in context
            else str(uuid.uuid1()),
            type=self.config["type"],
            time=context["time"]
            if isinstance(context, dict) and "time" in context
            else datetime.now().isoformat(),
            source=self.config["source"],
            sourcehost=self.config["sourcehost"],
            minorversion=0,
            data=obj_as_dict,
        )
        return avro_record

    def serialize(self, obj) -> bytes:
        """
        Convert from attrs to a valid avro record.
        """
        avro_record = self.to_dict(obj)
        # Try to serialize using the generated schema.
        out = io.BytesIO()
        fastavro.schemaless_writer(out, self._schema_dict, avro_record)
        out.seek(0)
        return out.read()

    def extension_serializer(self, _, field, value):
        """
        Callback passed in as "value_serializer" arg in attr.asdict function.
        Serializes values for which an extention exists in self.extensions dict.
        """
        extension = self.extensions.get(field.type, None)
        if extension is not None:
            return extension.serialize(value)
        return value

    def deserialize(self, data: bytes, writer_schema=None) -> object:
        """
        Deserializes data into self.attrs_cls instance
        # TODO document writer schema
        """
        data_file = io.BytesIO(data)
        if writer_schema is not None:
            record = fastavro.schemaless_reader(
                data_file, writer_schema, self._schema_dict
            )
        else:
            record = fastavro.schemaless_reader(data_file, self._schema_dict)
        return self.dict_to_attrs(record["data"], self._attrs_cls)

    def dict_to_attrs(self, data: dict, attrs_cls):
        """
        This function mutates the incoming `data` dict argument that's
        passed in.
        """
        for attribute in attrs_cls.__attrs_attrs__:
            if attribute.name in data:
                sub_data = data[attribute.name]
                if sub_data is None:
                    # delete keys that have defaults in attr class and which have None as value
                    # this is to let attr class take care of creating default values
                    if attribute.default is not attr.NOTHING:
                        del data[attribute.name]
                else:
                    if hasattr(attribute.type, "__attrs_attrs__"):
                        if attribute.name in data:
                            data[attribute.name] = self.dict_to_attrs(
                                sub_data, attribute.type
                            )
                    elif attribute.type in self.extensions:
                        extension = self.extensions.get(attribute.type)
                        if attribute.name in data:
                            data[attribute.name] = extension.deserialize(sub_data)
                        else:
                            raise Exception(
                                f"Necessary key: {attribute.name} not found in data dict"
                            )
                    elif attribute.type not in AVRO_TYPE_FOR:
                        raise TypeError(
                            f"Unable to deserialize {attribute.type} data, please add extension for custom data type"
                        )

        return attrs_cls(**data)


class KafkaWrapper(AvroAttrsBridge):
    """
    Wrapper class to help AvroAttrsBridge to work with kafka.

    confluent_kafka::AvroSerializing needs a callable input that converts obj to avro dict. The callback needs to take in obj and kafka context.

    confluent_kafka::AvroDeSerializing needs a callable input that converts avro dict into obj. The callback needs to take in data (avro record dict) and kafka context.
    """

    def to_dict(self, obj, _context):
        return super().to_dict(obj)

    def from_dict(self, data, _context):
        return self.dict_to_attrs(data["data"], self._attrs_cls)

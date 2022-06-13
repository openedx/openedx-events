Purpose
-------
Used to automate the conversion from event data dictionaries to Avro record dictionaries and back.

Note: This library does not handle serialization of Avro records down to byte representation and back. To do that we are relying on the event bus technology itself. It is however possible to use this library in conjunction with fastavro to do the full de/serialization to bytes and back if the event bus implementation does not do that for you (an example of this is provided in the test_utilities module).


Glossary
--------

Signal
    An instance of OpenEdxPublicSignal.
Event data
    A dictionary whose structure is determined by the init_data attribute of an instance of OpenEdxPublicSignal. Event data is sent via a call to ``MY_SIGNAL.send_event(**event_data)``.
Avro schema
    A specification describing the expected field names and types in an Avro record dictionary. See https://avro.apache.org/docs/current/spec.html
Avro record dictionary
    A dictionary whose structure is determined by an Avro schema. These dictionaries are the entities that are actually serialized to bytes and sent over the wire to the event bus.


Serialization
~~~~~~~~~~~~~
The ``to_dict`` method on the AvroSignalSerializer is used to convert
events to Avro records.

The ``schema_dict`` property can be used to configure an Avro-based serializer
for use with an event bus.


Deserialization
~~~~~~~~~~~~~~~
The ``from_dict`` method on the AvroSignalDeserializer is used to convert
Avro records to event data dictionaries.

Similar to AvroSignalSerializer, the``schema_dict`` property can be used to
configure an Avro-based deserializer for use with an event bus.

To deserialize bytes that have come over the wire on the event bus, and then
emit the event to the relevant listeners, you will need to know the event_type
of the original signal. This can be sent over as a message header or as other
event metadata, depending on the bus implementation.

Custom types
~~~~~~~~~~~~

By default, this module supports de/serialization of attrs-decorated classes,
Avro-primitive equivalents (see types.py), and some other classes specified in
``custom_serializers.DEFAULT_CUSTOM_SERIALIZERS``

If your event uses other data types, you will need to create custom de/serializers. To do this, you will need to extend the
BaseCustomTypeAvroSerializer with a class that handles your particular data type.
If the new type is cross-platform, it may make sense to add it to ``DEFAULT_CUSTOM_SERIALIZERS``.
Otherwise, you will need to extend the AvroSignalSerializer and AvroSignalDeserializer classes,
in particular overriding the custom_type_serializers method to return your custom
serializer.


.. code-block:: python

 class MyAvroSerializer(BaseCustomTypeAvroSerializer):

    cls = MyClass
    field_type = PYTHON_TYPE_TO_AVRO_MAPPING[str]

    @staticmethod
    def serialize(obj) -> str:
        str(MyClass)

    @staticmethod
    def deserialize(data: str):
        MyClass.fromString(data)

 class MySignalSerializer(AvroSignalSerializer):
    def custom_type_serializers(self):
        return [MyAvroSerializer]

 class MySignalDeserializer(AvroSignalDeserializer):
    def custom_type_serializers(self):
        return [MyAvroSerializer]

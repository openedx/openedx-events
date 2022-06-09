Purpose
-------
Used to automate the following conversions:

event data => Avro record (dict) => bytes
bytes => Avro record (dict) => event data

Essentially, helps serialize and deserialize events data specified in openedx-events repository.

Glossary
--------

Signal - An instance of OpenEdxPublicSignal.
Event data - A dictionary whose structure is determined by the init_data attribute of an instance of OpenEdxPublicSignal. Event data is sent via a call to MY_SIGNAL.send_event(**event_data).
Avro schema - A specification describing the expected field names and types in an Avro record dictionary
Avro record dictionary - A dictionary whose structure is determined by an Avro schema. These dictionaries are the entities that are actually serialized to bytes and sent over the wire to the event bus.


How To Use
----------
Serializer
~~~~~~~~~~
To create an event serializer for a signal:

.. code-block:: python

    USER_SIGNAL = OpenEdxPublicSignal(
        event_type="simple.signal",
        data={"user": UserData}
    )
    event_serializer = AvroSignalSerializer(USER_SIGNAL)


You can then use the ``to_dict`` method on the serializer to convert events to avro records,
as well as the ``schema_dict`` property to configure an Avro-based serializer
for use with an event bus.

For example, to serialize a COURSE_ENROLLMENT_CREATED event to bytes (eventually to
be published to the event bus)

.. code-block:: python

   enrollment_serializer = AvroSignalSerializer(COURSE_ENROLLMENT_CREATED)
   enrollment_object = CourseEnrollmentData(...enrollment_data)
   out = io.BytesIO()
   data_dict = enrollment_serializer.to_dict({"enrollment": enrollment_object})
   fastavro.schemaless_writer(out, enrollment_serializer.schema_dict, data_dict)
   out.seek(0)
   return out.read()

Deserializer
~~~~~~~~~~~~
To deserialize bytes that have come over the wire on the event bus, and then
emit the event to the relevant listeners, you will need to know the event_type
of the original signal. This can be sent over as a message header or as other event metadata, depending on the bus implementation.


.. code-block:: python

   my_signal = OpenEdxPublicSignal.get_signal_by_type(get_event_type())
   deserializer = AvroSignalDeserializer(my_signal)
   data_file = io.BytesIO(bytes_from_wire)
   as_dict = fastavro.schemaless_reader(data_file, deserializer.schema_dict)
   my_signal.send_event(**deserializer.from_dict(as_dict))

Custom types
~~~~~~~~~~~~
If your event data contains field types that are not attrs-decorated classes,
Avro-primitive equivalents (see types.py), CourseKeys, or datetimes, you will
need to create custom de/serializers. To do this, you will need to extend the
BaseCustomTypeAvroSerializer with a class that handles your particular data type.
You will then need to extend the AvroSignalSerializer and AvroSignalDeserializer classes,
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

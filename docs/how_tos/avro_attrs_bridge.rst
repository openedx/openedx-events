Avro Attrs bridge
=================

Purpose
-------
Used to automate the following conversions:

event data => Avro dict => bytes
bytes => Avro dict => event data

Essentially, helps serialize and deserialize events data specified in openedx-events repository.

How To Use
----------
To instantiate a bridge for a new signal

.. code-block:: python

    USER_SIGNAL = OpenEdxPublicSignal(
        event_type="simple.signal",
        data={"user": UserData}
    )
    user_data_bridge = AvroAttrsBridge(USER_SIGNAL)

_OEP 41: https://open-edx-proposals.readthedocs.io/en/latest/architectural-decisions/oep-0041-arch-async-server-event-messaging.html#fields

You can then use the ``from_dict`` and ``to_dict`` methods on the bridge,
as well as the ``schema_dict`` property to configure an Avro-based de/serializer
to correctly serialize and deserialize events to be sent by the signal.

For example, to serialize a COURSE_ENROLLMENT_CREATED event (eventually to
be published to the event bus)

.. code-block:: python

   enrollment_bridge = AvroAttrsBridge(COURSE_ENROLLMENT_CREATED)
   enrollment_object = CourseEnrollmentData(...enrollment_data)
   out = io.BytesIO()
   data_dict = enrollment_bridge.to_dict({"enrollment": enrollment_object})
   fastavro.schemaless_writer(out, bridge.schema_dict, data_dict)
   out.seek(0)
   return out.read()

To deserialize bytes that have come over the wire on the event bus, and then
emit the event to the relevant listeners, you will need to know the event_type
of the original signal. This can be sent over as a message header or event
topic or other metadata, depending on the bus implementation.

.. code-block:: python

   my_signal = OpenEdxPublicSignal.get_signal_by_type(get_event_type())
   bridge = AvroAttrsBridge(my_signal)
   data_file = io.BytesIO(bytes_from_wire)
   as_dict = fastavro.schemaless_reader(data_file, bridge.schema_dict)
   my_signal.send_event(**bridge.from_dict(as_dict))


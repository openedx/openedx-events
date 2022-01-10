===================================
Attrs event data conversion to Avro
===================================
.. contents::

1 Context
---------

- `0003-events-payload.rst <https://github.com/eduNEXT/openedx-events/blob/main/docs/decisions/0003-events-payload.rst#decisions>`_: Openedx has standardized around using attrs classes to define event data.

- `OEP-52: Event Bus (Draft) <https://github.com/openedx/open-edx-proposals/pull/233>`_:  Openedx is testing out event bus technology for communication between services and within services. We are currently trialing Kafka.

- The industry standard for messaging format used with Kafka is Avro (there are other options, but Avro has been the standard for a while). In decision `open-edx-proposals/oep-0052/001-schema-representation.rst <https://github.com/openedx/open-edx-proposals/blob/7bf9acedae5f4290ac2d0e4374c3078278842801/oeps/architectural-decisions/oep-0052/decisions/001-schema-representation.rst>`_: We decided to create a bridge class to convert from Attrs data class to Avro specification.

The purpose of this ADR is to document decisions made while developing `AvroAttrsBridge <https://github.com/eduNEXT/openedx-events/blob/main/openedx_events/avro_attrs_bridge.py>`_ class.

1.1 Some relavant info about `Attrs <https://www.attrs.org/en/stable/examples.html>`_ decorated classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. attrs allows you to serialize instances of attrs classes to dicts using attrs.asdict. Though at default, this only works for data types that are JSON serializable.

   1. For complex data types (like datetime), you can pass a value\_serializer hook to attr.asdict, such as (`docs on asdict <https://www.attrs.org/en/stable/extending.html?highlight=value_serializer#customize-value-serialization-in-asdict>`_):

      .. code:: python

          from attr import asdict
          def serialize(inst, field, value):
              if isinstance(value, datetime.datetime):
                  return value.isoformat()
              return value

          data = asdict(
              Data(datetime.datetime(2020, 5, 4, 13, 37)),
              value_serializer=serialize,
          )

          data
          # output; {'dt': '2020-05-04T13:37:00'}
          json.dumps(data)
          # output:'{"dt": "2020-05-04T13:37:00"}'

2. Each attrs-decorated class has a attrs\_attrs class attribute (`source attrs docs <https://www.attrs.org/en/stable/extending.html#extending>`_). It’s a tuple of attrs.Attribute carrying metadata about each attribute.
   You can get \`type\` info on everything datum defined in an attrs class.

   .. code:: python

       @attr.s()
       class Example:
           datum1= attr.ib(type=str)
           datum2= attr.ib(type=int)
           time= attr.ib(type=datetime)

       print(Example.__attrs_attrs__[0].type)
       # <class 'str'>
       print(Example.__attrs_attrs__[1].type)
       # <class 'int'>
       print(Example.__attrs_attrs__[2].type)
       # <class 'datetime.datetime'>

3. attrs-decorated classes allow defaults

   .. code:: python


       class Example:
           datum2= attr.ib(type=int)
           time= attr.ib(type=datetime)
           datum1= attr.ib(type=str, default="default")

       example_as_dict = { 'datum2': 1, time: datetime.now()} # there is no value for datum1
       print(Example(...example_as_dict))
       # Example(datum2=1, time=datetime.datetime(2022, 1, 7, 14, 1, 51, 672141), datum1='default')

1.2 Some relevant info about Avro specification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. An Avro schema is represented in JSON

2. Avro specifies two serialization encodings: binary and JSON.
   Binary encoding is smaller and faster. Binary encoding does not include field names, self-contained information about the types of individual bytes, nor field or record separators. Therefore readers are wholly reliant on the schema used when the data was encoded.

3. A schema must be used to deserialize encoded data.
   The encoded data does not include type or field names. To read the data, the schema used to read the data must be identical to the schema used to write data.

4. evolution requirements

   - Avro can handle some schema evolution. When schema has evolved, to read encoded data with older version of schema, both new version and old version must be passed into the reader.

   - Case \`Adding a new field\`: A default value can be specified for a field in the Avro schema. This value is only used when reading instances that lack field. This default does not make field optional at encoding time.

2 Decision
----------

Each AvroAttrsBridge class will support:

1. Creation of Avro Schema of the attrs\_cls arg at instantiation
   It will throw an exception if unable to create Avro Schema

2. Convert attrs\_cls object into a dict that follow the Avro Schema for attrs\_cls

3. Serialize attrs\_cls object into a byte string that represents that object
   This is done through following transformations:
   attrs\_cls object -> dict (avro schema) -> byte array (avro schema)

4. Convert byte string representing attrs\_cls object into dict that follows the Avro Schema

5. Converts byte string representation of the attrs\_cls object into attrs\_cls object

6. Support doing the above by default for all attrs decorated classes in openedx-events repository

7. Provide ability to extend AvroAttrsBridge to support any attrs decorated classes outside of openedx-events repository

8. Follow cloudevents specification as stated in OEP-TODO


AvroAttrsBridge is generalized to serialize/deserialize  basic attrs decorated class. Any specific Kafka requirements will be implemented in KafkaWrapper class, a subclass of AvroAttrsBridge.

2.1 How to extend AvroAttrsBridge class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

At defult, attrs.asdict only supports basics types for conversion to dict (Basically, only things you could json.dump). To allow AvroAttrsBridge to work with custom classes, a function will be passed to  value\_serializer arg in attrs.asdict. The value_serializer function needs to be able to handle any custom classes used in an events attrs class.

To make is easier to developers, an extensions interface has been implemented into AvroAttrsBridge.
To allow AvroAttrsBridge to work with these classes, you can pass in an extensions keyword to AvroAttrsBridge. The extensions keyword expects a dict with following format: {<type of custom class>: <AvroAttrsBridgeExtention subclass for custom class>}

The AvroAttrsBridgeExtention subclass should have the following methods:

1. serialize(obj)
   serializes \`obj\` (a instance of custom class)

2. deserialize(data: str)
   converts \`data\` back to instance of custom class. The data str should have been created by self.serialize method.

3. record\_fields
   returns the avro schema for this custom class. Usually, this is just a str


Lots of attrs decorated classes in openedx-events repository have data with custom class types. AvroAttrsBridge class comes with default\_extensions which should hold AvroAttrsBridgeExtention classes for each of those custom classes. If you find any default\_extensions in AvroattrsBridge is missing a custom class, please add it yourself or reach out to the developers of the repository!

2.2 Handling Evolution
~~~~~~~~~~~~~~~~~~~~~~

If an attrs decorated class has a default value for one of its attributes, avro\_attrs\_bridge will assume that attribute is optional. This is to allow attrs events to change over time. If you want to add a new attribute to old attrs decorated class, please set a default value for it so that data created using old version can still be read.

This has not been tested that well, so if you do some testing, please update this and create further how\_tos to handle schema evolution.

3 Open Questions
----------------

3.1 What should go in config?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

AvroAttrsBridge allows you to config the following values. It provides some default value for testing, but those should not be used in production.

- source:  This field will be used to indicate the logical source of an event, and will be of the form /{namespace}/{service}/{web|worker}. All services in standard distribution of Open edX should use openedx for the namespace. Examples of services might be “discovery”, “lms”, “studio”, etc. The value “web” will be used for events emitted by the web application, and “worker” will be used for events emitted by asynchronous tasks such as celery workers.
  For more info, see OEP-41: Asynchronous Server Event Message Format

- sourcehost: should represent the physical source of message. i.e. host identifier of the server that emitted this event (example: edx.devstack.lms)

- type: The name of event.
  Should be formatted \`{Reverse DNS}.{Architecture Subdomain}.{Subject}.{Action}.{Major Version}\`.

For more info about above, see `OEP- 41: Asynchronous Server Event Message Format <https://open-edx-proposals.readthedocs.io/en/latest/architectural-decisions/oep-0041-arch-async-server-event-messaging.html#fields>`_

3.2 How well does schema evolution work?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Basic schema evolution has been tested in unit tests in openedx\_events/tests/test\_avro\_attrs\_bridge.py, but schema evolution has not be testing out in the field.

3.2.1 What handles versioning?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

AvroAttrsBridge does not handle versioning logistics.

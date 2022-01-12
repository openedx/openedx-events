Avro Attrs bridge
=================

.. contents::

Purpose
-------

Used to automate the following conversions:

attrs class => Avro Dict => Bytes
Bytes => Avro Dict => attrs class

Essentially, helps serialize and deserialize events data specified in openedx-events repository.

How To Use
----------

If you want to go from attrs obj to serialized bytes and back:

.. code-block:: python

   from openedx_events.learning.data import UserData
   from openedx_events.avro_attrs_bridge import AvroAttrsBridge

   config = {
        "source": "/openedx/lms/web",
        "sourcehost": "edx.devstack.lms",
        "type": "org.openedx.learning.student.registration.completed.v1",
    }

   user_data_bridge = AvroAttrsBridge(AvroAttrsBridge, config)
   user_data_object = UserData(...) # create object
   serialied_user_data = user_data_bridge.serialize(user_data_object)
   deserialize_user_data = user_data_bridge.deserealize(serialied_user_data)
   assert deserealize_user_data == user_data_object



To learn more about what is in config, see Fields in `OEP 41`_:Asynchronous Server Event Message Format.

.. _OEP 41: https://open-edx-proposals.readthedocs.io/en/latest/architectural-decisions/oep-0041-arch-async-server-event-messaging.html#fields


If you want to go from attrs obj to avro dict and back:

.. code-block:: python

   from openedx_events.learning.data import UserData
   from openedx_events.avro_attrs_bridge import AvroAttrsBridge

   config = {
        "source": "/openedx/lms/web",
        "sourcehost": "edx.devstack.lms",
        "type": "org.openedx.learning.student.registration.completed.v1",
    }

   user_data_bridge = AvroAttrsBridge(AvroAttrsBridge, config)
   user_data_object = UserData(...) # create object
   user_data_dict = user_data_bridge.to_dict(user_data_object)
   user_data_new_object = user_data_bridge.dict_to_attrs(user_data_dict)
   assert deserealize_user_data == user_data_new_object


How to extend AvroAttrsBridge class
-----------------------------------

At default, attrs.asdict only supports basics types for conversion to dict (Basically, only things you could json.dump). To allow AvroAttrsBridge to work with non-primitive types, a function will be passed to  value_serializer arg in attrs.asdict. The value_serializer function needs to be able to handle any non-primitive types used in an events attrs class.

To make is easier to developers, an extensions interface has been implemented into AvroAttrsBridge.
To allow AvroAttrsBridge to work with these classes, you can pass in a dict to the extensions keyword to AvroAttrsBridge. The extensions keyword expects a dict with following format: {<type of non-primitive>: <AvroAttrsBridgeExtention subclass for non-primitive>}

The AvroAttrsBridgeExtention subclass should have the following methods:

1. serialize(obj)
   serializes \`obj\` (a instance of non-primitive)

2. deserialize(data: str)
   converts \`data\` back to instance of non-primitive. The data str should have been created by self.serialize method.

3. record_fields
   returns the avro schema for this non-primitive. Usually, this is just a str


AvroAttrsBridge class comes with default_extensions which should hold AvroAttrsBridgeExtention classes for all the non-primitive types necessary to work with all attrs-decorated classes defined in openedx_events.

If you find default_extension for a non-primitive type (used in openedx_events) is missing, please add it yourself or reach out to the developers of the repository!

Handling Schema Evolution
-------------------------

If an attrs decorated class has a default value for one of its attributes, avro_attrs_bridge will assume that attribute is optional. This is to allow attrs events to change over time. If you want to add a new attribute to old attrs decorated class, please set a default value for it so that data created using old version can still be read.

This has not been tested in production. If you do some testing, please update this and create further how_tos to handle schema evolution.


context
-------

Some relavant info about `Attrs <https://www.attrs.org/en/stable/examples.html>`_ decorated classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. attrs allows you to serialize instances of attrs classes to dicts using attrs.asdict. Though at default, this only works for data types that are JSON serializable.

   1. For non-primitive types (like datetime), you can pass a value_serializer hook to attr.asdict, such as (`docs on asdict <https://www.attrs.org/en/stable/extending.html?highlight=value_serializer#customize-value-serialization-in-asdict>`_):

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

2. Each attrs-decorated class has a attrs_attrs class attribute (`source attrs docs <https://www.attrs.org/en/stable/extending.html#extending>`_). It’s a tuple of attrs.Attribute carrying metadata about each attribute.
   You can get `type` info on every field defined in an attrs-decorated class.

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

Some relevant info about Avro specification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. An Avro schema is represented in JSON

2. Avro specifies two serialization encodings: binary and JSON.

   Binary encoding is smaller and faster. Binary encoding does not include field names, self-contained information about the types of individual bytes, nor field or record separators. Therefore readers are wholly reliant on the schema used when the data was encoded.

3. Avro deals with conversion between "dict" like objects to bytes.

   So our solution needs to go from attrs decorated classes to "dict" like objects

3. A schema must be used to deserialize encoded data.

   The encoded data does not include type or field names. To read the data, the schema used to read the data must be identical to the schema used to write data.

4. evolution requirements

   - Avro can handle some schema evolution. When schema has evolved, to read encoded data with older version of schema, both new version and old version must be passed into the reader.

   - Case: Adding a new field: A default value can be specified for a field in the new Avro schema. This would allow you to continue reading data produced with older schema.

     Note: This default value is only used when reading instances that lack field. This default does not make field optional at encoding time.

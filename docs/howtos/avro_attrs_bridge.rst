Avro Attrs bridge
=================

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

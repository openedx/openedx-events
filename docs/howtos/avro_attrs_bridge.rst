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

========================================
AvroAttrsBridge implementation decisions
========================================
.. contents::

Context
-------

- `0003-events-payload.rst <https://github.com/eduNEXT/openedx-events/blob/main/docs/decisions/0003-events-payload.rst#decisions>`_: Openedx has standardized around using attrs classes to define event data.

- `OEP-52: Event Bus (Draft) <https://github.com/openedx/open-edx-proposals/pull/233>`_:  Openedx is testing out event bus technology for communication between services and within services. We are currently trialing Kafka.

- The industry standard for messaging format used with Kafka is Avro (there are other options, but Avro has been the standard for a while). In decision `open-edx-proposals/oep-0052/001-schema-representation.rst <https://github.com/openedx/open-edx-proposals/blob/7bf9acedae5f4290ac2d0e4374c3078278842801/oeps/architectural-decisions/oep-0052/decisions/001-schema-representation.rst>`_: We decided to create a bridge class to convert from Attrs data class to Avro specification.

The purpose of this ADR is to document decisions made while developing `AvroAttrsBridge <https://github.com/eduNEXT/openedx-events/blob/main/openedx_events/avro_attrs_bridge.py>`_ class.


Decision
--------

Each AvroAttrsBridge class will support:

1. Avro Schema creation is validated at instatiation.

   Schema is created in the __init__ function.

2. Allows for following conversions:

   attrs decorated class object => dict => Avro encoded string => dict => attrs decorated class object

3. Support doing the above by default for all attrs decorated classes in openedx-events repository

4. Provide ability to extend AvroAttrsBridge to support any attrs decorated classes outside of openedx-events repository

5. Follow cloudevents specification as stated in `OEP-41`_: Asynchronous Server Event Message Format.


AvroAttrsBridge is generalized to serialize/deserialize  basic attrs decorated class. Any specific Kafka requirements will be implemented in KafkaWrapper class, a subclass of AvroAttrsBridge.


Open Questions
--------------

What should go in config?
~~~~~~~~~~~~~~~~~~~~~~~~~

AvroAttrsBridge allows you to config the following values. It provides some default value for testing, but those should not be used in production.

- source:  This field will be used to indicate the logical source of an event, and will be of the form /{namespace}/{service}/{web|worker}. All services in standard distribution of Open edX should use openedx for the namespace. Examples of services might be “discovery”, “lms”, “studio”, etc. The value “web” will be used for events emitted by the web application, and “worker” will be used for events emitted by asynchronous tasks such as celery workers.
  For more info, see OEP-41: Asynchronous Server Event Message Format

- sourcehost: should represent the physical source of message. i.e. host identifier of the server that emitted this event (example: edx.devstack.lms)

- type: The name of event.
  Should be formatted \`{Reverse DNS}.{Architecture Subdomain}.{Subject}.{Action}.{Major Version}\`.

For more info about above, see `OEP-41`_: Asynchronous Server Event Message Format

.. _OEP-41: https://open-edx-proposals.readthedocs.io/en/latest/architectural-decisions/oep-0041-arch-async-server-event-messaging.html#fields>


How to coordinate schema evolution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

AvroAttrsBridge does not handle versioning logistics.

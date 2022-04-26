5. External Event Schema Format
===============================

Status
------

Provisional


Context
-------

* It is a best practice to use an explicit schema definition. Avro is the recommended serialization format for Kafka.

* The attrs objects that we currently have for signal-based events don't easily inter-operate with event bus client objects. Source ADR ":doc:`0003-events-payload`".

* Industry best practices seem to suggest using a binary encoding of messages.

* Industry best practice also suggests using AVRO over JSONSchema for better expression around schema evolution.

* Even if we use a JSON encoding for the message we'll probably want to enable compression on the wire to reduce data
  size.  This would mean whether or not we use JSON encoding is moot because the data on the wire will still be binary
  encoded.

Decision
--------

* We will continue favoring ``attrs`` decorated classes for explicit schema definitions for signals

* We will also use the binary serialization of messages that are transmitted over the event bus.

* The binary encoding of messages will use AVRO specification.

* A new utility will be created to auto generate Avro schema from the ``init_dict`` property of an OpenEdxPublicSignal instance

  * Out of the box, bridge will generate schemas for ``attrs`` decorated classes and Avro primitives
  * Developers will be able to create extensions to the bridge to make it handle non-attrs, non-primitive classes

Implementation Notes
--------------------

`AvroAttrsBridge`_ class is a potential approach to this using the `built-in metadata`_ that the ``attrs`` library provides for extending ``attrs``.

.. _AvroAttrsBridge: https://github.com/openedx/openedx-events/blob/main/openedx_events/bridge/avro_attrs_bridge.py
.. _built-in metadata: https://www.attrs.org/en/stable/extending.html

Consequences
------------

* There will be bridging code that will abstract away schema generation from most developers of events.  This may have a negative impact as it might make it harder for developers to reason about schema evolution.

* For non-primitive, non-attr types (eg. Opaque Keys objects), the bridging code between will need to have special serializers or clearly fail.

* Any reference to using JSON or JSONSchema in `OEP-41: Asynchronous Server Event Message Format`_ should be review and updated to clarify implied or explicit decisions that may be reversed by this decision.

* `OEP-41: Asynchronous Server Event Message Format`_ also dictates the use of the CloudEvents specification. Combined with this ADR, we would be required to adhere to the `CloudEvents Avro Format`_. There may also be additional CloudEvent related work tied to a particular protocol binding, like the `Kafka Protocol Binding for CloudEvents`_. This, however, is out of scope of this particular decision.

.. _`OEP-41: Asynchronous Server Event Message Format`: https://open-edx-proposals.readthedocs.io/en/latest/architectural-decisions/oep-0041-arch-async-server-event-messaging.html

.. _CloudEvents Avro Format: https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/formats/avro-format.md

.. _Kafka Protocol Binding for CloudEvents: https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/kafka-protocol-binding.md#3-kafka-message-mapping

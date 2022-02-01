1 Event bus as extension of django signals
------------------------------------------

1.1 Context
~~~~~~~~~~~

- Django Signals are widely used in edx-platform and elsewhere. OpenedX developers are familiar with Django Signals.

- Django Signals are much cheaper to send, and offer pretty much no additional work as compared to sending via Kafka.

- Django Signals don’t require extra infrastructure and are simpler for people to test with.

- We want to make it easy to integrate different event bus technologies


This decision came out based on following conversations:

- `#38: What to send over the wire (Kafka)? <https://github.com/eduNEXT/openedx-events/issues/38>`_

- `#39: ARCHBOM-2010: How does Event Bus interact with OpenedX Django Signals? <https://github.com/eduNEXT/openedx-events/issues/39>`_

1.2 Decision
~~~~~~~~~~~~

- Django signals will be the method for communication within an OpenedX Django service.
- An external event bus will be used to transport messages between services.
- For production of messages, the external event bus will hook onto a django service as another django app. The Event Bus app will listen for relevant django signals, convert them to event bus's format (using AvroAttrsBridge), and send the messages over the wire.
- For consumption, the event bus implementation will convert the messages back into django signals and emit them.
  - The exact design of the consuming event bus implementation is unclear at this time.

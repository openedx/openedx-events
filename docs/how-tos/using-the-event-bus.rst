Using the Open edX Event Bus
============================

After creating a new Open edX Event, you might need to send it across services instead of just within the same process. For this kind of use-cases, you might want to use the Open edX Event Bus. Here :doc:`../concepts/event-bus` you can find useful information about the event bus.

The Open edX Event Bus is a key component of the Open edX architecture, enabling services to communicate without direct dependencies on each other. This guide provides an overview of how to use the event bus to broadcast Open edX Events to multiple services, allowing them to react to changes or actions in the system.

Prerequisites
-------------

Before you start using the event bus, you need to have the following:

- A service that will consume the event
- A service that will produce the event
- The Open edX Event Bus concrete implementation (Django plugin) installed in both services
- The message broker (e.g., Kafka or Redis) set up
- The Open edX Event Bus configuration set up in both services

Configurations
--------------

Here are the available configurations for the event bus we'll be using:

.. settings::
    :folder_path: openedx_events/event_bus

Setup
-----

To start producing and consuming events using the Open edX Event Bus, follow these steps:

#. **Produce the event**

In the producing/host application, include ``openedx_events`` in ``INSTALLED_APPS`` settings and add ``EVENT_BUS_PRODUCER_CONFIG`` setting. This setting is a dictionary of event_types to dictionaries for topic-related configuration. Each topic configuration dictionary uses the topic as a key and contains:

- A flag called ``enabled`` denoting whether the event will be published.
- The ``event_key_field`` which is a period-delimited string path to event data field to use as event key.

.. note:: The topic names should not include environment prefix as it will be dynamically added based on ``EVENT_BUS_TOPIC_PREFIX`` setting.

Here's an example of the producer configuration:

.. code-block:: python

   EVENT_BUS_PRODUCER_CONFIG = {
       'org.openedx.content_authoring.xblock.published.v1': {
           'content-authoring-xblock-lifecycle': {'event_key_field': 'xblock_info.usage_key', 'enabled': True},
           'content-authoring-xblock-published': {'event_key_field': 'xblock_info.usage_key', 'enabled': True}
       },
       'org.openedx.content_authoring.xblock.deleted.v1': {
           'content-authoring-xblock-lifecycle': {'event_key_field': 'xblock_info.usage_key', 'enabled': True},
       },
   }

The ``EVENT_BUS_PRODUCER_CONFIG`` is read by ``openedx_events`` and a handler is attached which does the leg work of reading the configuration again and pushing to appropriate handlers.

To let the openedx-events know about which event bus implementation to use (e.g., Kafka or Redis), you need to set the ``EVENT_BUS_PRODUCER`` setting. This setting should be the dotted path to the concrete implementation class.

#. **Consume the Event**

In the consuming service, include ``openedx_events`` in ``INSTALLED_APPS`` settings and add ``EVENT_BUS_CONSUMER_CONFIG`` setting. Then, you should implement a receiver for the event type you are interested in.


   .. code-block:: python

       @receiver(XBLOCK_DELETED)
       def update_some_data(sender, **kwargs):
       ... do things with the data in kwargs ...
       ... log the event for debugging purposes ...

To let the openedx-events know about which event bus implementation to use (e.g., Kafka or Redis), you need to set the ``EVENT_BUS_CONSUMER`` setting. This setting should be the dotted path to the concrete implementation class.

#. **Run the consumer**: Run the consumer process in the consuming service to listen for events.

#. **Send the event**: Send the event from the producing service.

#. **Check the consumer**: Check the consumer logs to see if the event was received.

.. TODO: add more details about how to run the consumer and send the event. https://github.com/openedx/openedx-events/blob/main/openedx_events/management/commands/consume_events.py

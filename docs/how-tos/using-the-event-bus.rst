Using the Open edX Event Bus
============================

After creating a new Open edX Event, you might need to send it across services instead of just within the same process. For this kind of use-cases, you might want to use the Open edX Event Bus. Here :doc:`../concepts/event-bus` you can find useful information about the event bus.

The Open edX Event Bus is a key component of the Open edX architecture, enabling services to communicate without direct dependencies on each other. This guide provides an overview of how to use the event bus to broadcast Open edX Events to multiple services, allowing them to react to changes or actions in the system.

Setup
-----

To start producing and consuming events using the Open edX Event Bus, follow these steps:

Install the Open edX Event Bus Plugin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First, you need to install the Open edX Event Bus plugin in both the producing and consuming services. The plugin is a Django app that provides the necessary tools and configurations to produce and consume events. You could install the Redis plugin by running:

.. code-block:: bash

   pip install edx-event-bus-redis

Configure the Event Bus
~~~~~~~~~~~~~~~~~~~~~~~

In :doc:`../reference/event-bus-configurations`, you can find the available configurations for the event bus that are used to set up the event bus in the Open edX platform.

In both the producing and consuming services, you need to configure the event bus. This includes setting up the event types, topics, and other configurations for the event bus. In this step, you should configure the producer and consumer classes for the event bus implementation you are using:

- In the producing service, configure the producer class by setting the ``EVENT_BUS_PRODUCER`` setting. E.g., ``edx_event_bus_redis.create_producer``.
- In the consuming service, configure the consumer class by setting the ``EVENT_BUS_CONSUMER`` setting. E.g., ``edx_event_bus_redis.RedisEventConsumer``.

By configuring these settings, you are telling Open edX Events which concrete implementation to use for producing and consuming events.

Produce the Event
~~~~~~~~~~~~~~~~~

In the producing/host application, include ``openedx_events`` in ``INSTALLED_APPS`` settings and add ``EVENT_BUS_PRODUCER_CONFIG`` setting. This setting is a dictionary of event_types to dictionaries for topic-related configuration. Each topic configuration dictionary uses the topic as a key and contains:

- A flag called ``enabled`` denoting whether the event will be published.
- The ``event_key_field`` which is a period-delimited string path to event data field to use as event key.

.. note:: The topic names should not include environment prefix as it will be dynamically added based on ``EVENT_BUS_TOPIC_PREFIX`` setting.

Here's an example of the producer configuration which will publish events for XBlock published and deleted events to the specified topics:

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

Consume the Event
~~~~~~~~~~~~~~~~~

In the consuming service, include ``openedx_events`` in ``INSTALLED_APPS`` settings and add ``EVENT_BUS_CONSUMER_CONFIG`` setting. Then, you should implement a receiver for the event type you are interested in. In this example, we are interested in the XBlock deleted event:

.. code-block:: python

   @receiver(XBLOCK_DELETED)
   def update_some_data(sender, **kwargs):
   ... do things with the data in kwargs ...
   ... log the event for debugging purposes ...

Run the Consumer
~~~~~~~~~~~~~~~~

To consume events, Open edX Events provides a management command called `consume_events`_ which can be called from the command line, how to run this command will depend on your deployment strategy. This command will start a process that listens to the message broker for new messages, processes them and emits the event.

You can find more a concrete example of how to produce and consume events in the `event-bus-redis`_ documentation.

.. _consume_events: https://github.com/openedx/openedx-events/blob/main/openedx_events/management/commands/consume_events.py
.. _event-bus-redis: https://github.com/openedx/event-bus-redis
.. _run the consumer locally without tutor: https://github.com/openedx/event-bus-redis/?tab=readme-ov-file#testing-locally
.. _run the consumer locally with tutor: https://github.com/openedx/event-bus-redis/blob/main/docs/tutor_installation.rst#setup-example-with-openedx-course-discovery-and-tutor

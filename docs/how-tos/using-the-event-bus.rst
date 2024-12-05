Using the Open edX Event Bus
============================

After creating a new Open edX Event, you might need to send it across services instead of just within the same process. For this kind of use-cases, you might want to use the Open edX Event Bus. Here :doc:`../concepts/event-bus`, you can find useful information to start getting familiar with the Open edX Event Bus.

The Open edX Event Bus is a key component of the Open edX architecture, enabling services to communicate without direct dependencies on each other. This guide provides an overview of how to use the event bus to broadcast Open edX Events to multiple services, allowing them to react to changes or actions in the system.

Setup
-----

To start producing and consuming events using the Open edX Event Bus, follow these steps:

Step 1: Install the Open edX Event Bus Plugin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First, you need to install the Open edX Event Bus plugin in both the producing and consuming services. The plugin is a Django app that provides the necessary tools and configurations to produce and consume events. You could install the Redis plugin by running:

.. code-block:: bash

   pip install edx-event-bus-redis

.. note:: There are currently two community-supported concrete implementations of the Open edX Events Bus, Redis (`event-bus-redis`_) and Kafka (`event-bus-kafka`_). Redis is the default plugin for the Open edX Event Bus, but you can also use Kafka depending on your requirements. If none of these implementations meet your needs, you can implement your own plugin by following the :doc:`../how-tos/add-new-event-bus-concrete-implementation` documentation.

Step 2: Configure the Event Bus
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In :doc:`../reference/event-bus-configurations`, you can find the available configurations for the event bus that are used to set up the event bus in the Open edX platform.

In both the producing and consuming services, you need to configure the event bus. This includes setting up the :term:`event types <Event Type>`, :term:`topics <Topic>`, and other configurations for the :term:`Event Bus` to work with. In this step, you should configure the producer and consumer classes for the event bus implementation you are using:

- In the :term:`producing <Producer>` service, configure the producer class by setting the ``EVENT_BUS_PRODUCER`` setting. E.g., ``edx_event_bus_redis.create_producer``.
- In the :term:`consuming <Consumer>` service, configure the consumer class by setting the ``EVENT_BUS_CONSUMER`` setting. E.g., ``edx_event_bus_redis.RedisEventConsumer``.

By configuring these settings, you are telling Open edX Events which concrete implementation to use for producing and consuming events.

Step 3: Produce the Event
~~~~~~~~~~~~~~~~~~~~~~~~~

In the producing/host application, include ``openedx_events`` in ``INSTALLED_APPS`` settings if necessary and add ``EVENT_BUS_PRODUCER_CONFIG`` setting. This setting is a dictionary of :term:`event types <Event Type>` to dictionaries for :term:`Topic` related configuration. Each :term:`Topic` configuration dictionary uses the topic as a key and contains:

- A flag called ``enabled`` denoting whether the event will be published.
- The ``event_key_field`` which is a period-delimited string path to event data field to use as event key.

.. note:: The topic names should not include environment prefix as it will be dynamically added based on ``EVENT_BUS_TOPIC_PREFIX`` setting.

Here's an example of the producer configuration which will publish events for XBlock published and deleted events to the specified :term:`Topic`:

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

The ``EVENT_BUS_PRODUCER_CONFIG`` is read by ``openedx_events`` and a handler (`general_signal_handler`_) is attached which does the leg work of reading the configuration again and pushing to appropriate handlers.

Step 4: Consume the Event
~~~~~~~~~~~~~~~~~~~~~~~~~

In the consuming service, include ``openedx_events`` in ``INSTALLED_APPS`` settings if necessary and add ``EVENT_BUS_CONSUMER_CONFIG`` setting. Then, you should implement a receiver for the event type you are interested in. In this example, we are interested in the XBlock deleted event:

.. code-block:: python

   @receiver(XBLOCK_DELETED)
   def update_some_data(sender, **kwargs):
   ... do things with the data in kwargs ...
   ... log the event for debugging purposes ...

Step 5: Run the Consumer
~~~~~~~~~~~~~~~~~~~~~~~~

To consume events, Open edX Events provides a management command called `consume_events`_ which can be called from the command line, how to run this command will depend on your deployment strategy. This command will start a process that listens to the message broker for new messages, processes them and emits the event. Here is an example using of a `consumer using Tutor hosted in Kubernetes`_.

You can find more a concrete example of how to produce and consume events in the `event-bus-redis`_ documentation.

.. _consume_events: https://github.com/openedx/openedx-events/blob/main/openedx_events/management/commands/consume_events.py
.. _event-bus-redis: https://github.com/openedx/event-bus-redis
.. _event-bus-kafka: https://github.com/openedx/event-bus-kafka
.. _run the consumer locally without tutor: https://github.com/openedx/event-bus-redis/?tab=readme-ov-file#testing-locally
.. _run the consumer locally with tutor: https://github.com/openedx/event-bus-redis/blob/main/docs/tutor_installation.rst#setup-example-with-openedx-course-discovery-and-tutor
.. _general_signal_handler: https://github.com/openedx/openedx-events/blob/main/openedx_events/apps.py#L16-L44
.. _consumer using Tutor hosted in Kubernetes: https://github.com/openedx/tutor-contrib-aspects/blob/master/tutoraspects/patches/k8s-deployments#L535-L588

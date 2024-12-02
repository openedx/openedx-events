Open edX Event Bus
==================

Overview
--------

The suggested strategy for cross-service communication in the Open edX ecosystem is through an event-based architecture implemented via the :term:`Event Bus`. This functionality used for asynchronous communication between services is built on top of sending Open edX Events (Open edX-specific Django signals) within a service.

What is the Open edX Event Bus?
-------------------------------

The :term:`Event Bus` implements an event-driven architecture that enables asynchronous communication between services using the `publish/subscribe messaging pattern`_ (pub/sub). In the Open edX ecosystem, the event bus is used to broadcast Open edX Events to multiple services, allowing them to react to changes or actions in the system. The event bus is a key component of the Open edX architecture, enabling services to communicate without direct dependencies on each other.

.. image:: ../_images/event-bus-overview.png
   :alt: Open edX Event Bus Overview
   :align: center

Why use the Open edX Event Bus?
-------------------------------

The :term:`Event Bus` can help us achieve loose coupling between services, replacing blocking requests between services and large sync jobs, leading to a faster, more reliable, and more extensible system. See event messaging architectural goals highlighted in :doc:`openedx-proposals:architectural-decisions/oep-0041-arch-async-server-event-messaging` to read more about its benefits. Here's a brief summary of some key points:

* **Eliminate Blocking, Synchronous Requests**: reduce site outages when services become overloaded with requests by replacing synchronous calls with asynchronous communication.
* **Eliminate Expensive, Delayed, Batch Synchronization**: replace expensive batch processing with near real-time data updates.
* **Reduce the need for Plugins**: reduce the computational load for plugins that don't need to run in the same process by allowing cross-service communication of lifecycle events.

How Does the Open edX Event Bus Work?
-------------------------------------

The Open edX platform uses the ``OpenEdxPublicSignals`` (Open edX-specific Django Signals) to send events within a service. The event bus extends these signals, allowing them to be broadcasted and handled across multiple services. That's how Open edX Events are used for internal and external communication. For more details on how these Open edX-specific Django Signals are used by the event bus, refer to the :doc:`../decisions/0004-external-event-bus-and-django-signal-events` Architectural Decision Record (ADR).

Open edX Events provides an abstract implementation of the `publish/subscribe messaging pattern`_ (pub/sub) which is the chosen pattern for the event bus implementation as explained in :doc:`openedx-proposals:architectural-decisions/oep-0052-arch-event-bus-architecture`. It implements two abstract classes, `EventProducer`_ and `EventConsumer`_ which allow concrete implementations of the event bus based on different message brokers, such as Pulsar.

This abstraction allows for developers to implement their own concrete implementations of the event bus in their own plugins. There are currently two implementations of the event bus, Redis (`event-bus-redis`_) and Kafka (`event-bus-kafka`_). Redis streams is a data structure that acts like an append-only log, and Kafka is a distributed event streaming application. Both implementations handle event production and consumption with technology specific methods.

Architectural Diagram
*********************

These diagrams show what happens when an event is sent to the event bus. The event sending workflow follows the same steps as explained in :ref:`events-architecture`, with a key difference: when configured, the event bus recognizes events and publish them to the message broker for consumption by other services.

Components
~~~~~~~~~~

* **Service A (Producer)**: The service that emits the event. Developers may have emitted this event in a key section of the application logic, signaling that a specific action has occurred.
* **Service B (Consumer)**: The service that listens for the event and executes custom logic in response.
* **OpenEdxPublicSignal**: The class that implements all methods used to manage sending the event. This class inherits from Django's Signals class and adds Open edX-specific metadata and behaviors.
* **Event Producer**: The class in the :term:`Producer` service that sends events to the event bus. The producer serializes the event data and enriches it with relevant metadata for the consumer.
* **Event Consumer**: The class in the :term:`Consumer` service that receives events from the event bus. The consumer deserializes the :term:`message <Message>` and re-emits it as an event with the data that was transmitted.
* **Message Broker**: The :term:`message broker <Message Broker>` is responsible for storing and delivering messages between the producer and consumer.
* **Event Bus Plugin**: The concrete implementation of the event bus (EventProducer and EventConsumer) based on a specific :term:`message broker <Message Broker>`, such as Pulsar. The plugin handles event production and consumption with technology-specific methods.

Workflow
~~~~~~~~

.. image:: ../_images/event-bus-workflow-service-a.png
   :alt: Open edX Event Bus Workflow (Service A)
   :align: center

**From Service A (Producer)**

1. When the event is sent, a registered event receiver `general_signal_handler`_ is called to send the event to the event bus. This receiver is registered by the Django Signal mechanism when the ``openedx-events`` app is installed, and it listens for all Open edX Events.
2. The receiver checks the ``EVENT_BUS_PRODUCER_CONFIG`` to look for the ``event_type`` of the event that was sent.
3. If the event type is found and it's enabled for publishing in the configuration, the receiver obtains the configured producer class (``EventProducer``) from the concrete event bus implementation. For example, the producer class for Redis or Kafka implemented in their respective plugins.
4. The ``EventProducer`` serializes the event data and enriches it with relevant metadata, and then transforms it into a message that can be transmitted.
5. The producer uses its technology-specific ``send`` method to publish a message to the configured broker (e.g., Redis or Kafka).

.. image:: ../_images/event-bus-workflow-service-b.png
   :alt: Open edX Event Bus Workflow (Service B)
   :align: center

**From Service B (Consumer)**

1. A :term:`Worker` process in Service B runs indefinitely, checking the broker for new messages.
2. When a new message is found, the ``EventConsumer`` deserializes the message and re-emits it as an event with the data that was transmitted.
3. The event sending and processing workflow repeats in Service B.

This approach of producing events via settings with the generic handler was chosen to allow for flexibility in the event bus implementation. It allows developers to choose the event bus implementation that best fits their needs, and to easily switch between implementations if necessary. See more details in the :doc:`../decisions/0012-producing-to-event-bus-via-settings` Architectural Decision Record (ADR).

How is the Open edX Event Bus Used?
-----------------------------------

The event bus is used to broadcast Open edX Events to multiple services, allowing them to react to changes or actions in the system.

We encourage you to review the :doc:`../reference/real-life-use-cases` page for examples of how the event bus is used in the Open edX ecosystem by the community. Also, see the :doc:`../how-tos/using-the-event-bus` guide to get start sending events to the event bus.

.. _general_signal_handler: https://github.com/openedx/openedx-events/blob/main/openedx_events/apps.py#L16-L44
.. _EventProducer: https://github.com/openedx/openedx-events/blob/main/openedx_events/event_bus/__init__.py#L71-L91
.. _EventConsumer: https://github.com/openedx/openedx-events/blob/main/openedx_events/event_bus/__init__.py#L128-L139
.. _publish/subscribe messaging pattern: https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern
.. _event-bus-redis: https://github.com/openedx/event-bus-redis/
.. _event-bus-kafka: https://github.com/openedx/event-bus-kafka/

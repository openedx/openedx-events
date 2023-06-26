11. Enable producing to event bus via settings
##############################################

Status
******

**Accepted** 2023-06-05

Context
*******

The initial implementation of the event bus allowed only a single event type to be published to a `topic`_/`stream`_, with details like topic/stream name, consumer group name, and consumer name configured via code. We weren't sure what the API would finally look like, and whether the event bus config would live as part of the definition of the event, so we just went with explicit code that we could iterate upon.

The current implementation of openedx-events does not actually push any events to the underlying implementations like `edx-event-bus-kafka`_ and `edx-event-bus-redis`_. The event-producing application is expected to create a signal handler (since openedx-events subclasses Django signals) to catch the event and push it into the event bus. Some examples of the handlers: `handlers example`_.

.. _handlers example: https://github.com/openedx/edx-platform/blob/27b8d2f68d5dfaf84755e7d7f8dccc97ce3be509/cms/djangoapps/contentstore/signals/handlers.py#L162-L210
.. _edx-event-bus-kafka: https://github.com/openedx/event-bus-kafka
.. _edx-event-bus-redis: https://github.com/openedx/event-bus-redis
.. _topic: https://developer.confluent.io/learn-kafka/apache-kafka/topics/#kafka-topics
.. _stream: https://redis.io/docs/data-types/streams/

This ADR aims to propose a solution for configuring the details, like the topic name, consumer group name, etc. via Django settings as well as pushing events to the event bus without requiring the producing application to write additional handlers.


Decision
********

Create a generic signal handler to push events to the event bus. This handler should be attached to or connected to the signals that are enabled in Django settings. The configuration format will be as shown below:

.. code-block:: python

   # .. setting_name: EVENT_BUS_PRODUCER_CONFIG
   # .. setting_default: {}
   # .. setting_description: Dictionary of event_types to lists of dictionaries for topic related configuration.
   #    Each topic configuration dictionary contains a flag called `enabled` denoting whether the event will be
   #    published to the topic, topic/stream name called `topic` where the event will be pushed to,
   #    `event_key_field` which is a period-delimited string path to event data field to use as event key.
   #    Note: The topic names should not include environment prefix as it will be dynamically added based on
   #    EVENT_BUS_TOPIC_PREFIX setting.
   EVENT_BUS_PRODUCER_CONFIG = {
       'org.openedx.content_authoring.xblock.published.v1': [
           {'topic': 'content-authoring-xblock-lifecycle', 'event_key_field': 'xblock_info.usage_key', 'enabled': True},
           {'topic': 'content-authoring-xblock-published', 'event_key_field': 'xblock_info.usage_key', 'enabled': False},
       ],
       'org.openedx.content_authoring.xblock.deleted.v1': [
           {'topic': 'content-authoring-xblock-lifecycle', 'event_key_field': 'xblock_info.usage_key', 'enabled': True},
       ],
   }

This configuration will be read in openedx_events ``apps.OpenedxEventsConfig(AppConfig).ready`` method and a generic signal handler will be connected to the event_types (keys) listed in the configuration after validating its format.

.. code-block:: python

   def ready(self):
       load_all_signals()
       config = read_config()
       # validate the config dictionary and raise errors if any
       validate_config()
       for configured_signal in config:
           connect_or_disconnect_handlers(configured_signal)

The generic handler will again read the configuration and get details for event or signal triggered and push it to the event bus.

.. code-block:: python

   def general_signal_handler(sender, signal, **kwargs):
       config = read_config(signal)
       for topic in topics:
           push_event_to_implementation(signal, config)

The `push_event_to_implementation` function is the same code currently used in the `hard-coded handlers`_, the only difference is that it will read the details from the configuration.

Finally, replace the `handlers`_ in edx-platform with a default configuration that will configure and enable the same events as the handlers.

.. _handlers: https://github.com/openedx/edx-platform/blob/27b8d2f68d5dfaf84755e7d7f8dccc97ce3be509/cms/djangoapps/contentstore/signals/handlers.py#L162-L210
.. _hard-coded handlers: https://github.com/openedx/edx-platform/blob/27b8d2f68d5dfaf84755e7d7f8dccc97ce3be509/cms/djangoapps/contentstore/signals/handlers.py#L167-L171

Consequences
************

* Applications producing to event_bus can push events without requiring any additional code.
* Users can push multiple related event_types to the same topic, which will allow them to run a single consumer and process the events in the correct order.
* The configuration is a dictionary, which makes it flexible but difficult to enforce schemas and maintain them.
* Producing applications similar to consuming applications will be required to add ``openedx_events`` as an application in their ``INSTALLED_APPS`` settings.

Rejected Alternatives
*********************

* Implementing configurable handlers in the host applications, rather than in the shared library, will require repeating the code in each host application.
* Following the current way of using fixed handlers will restricts users ability to combine events in a single topic based on their preference, as well as stopping users from producing additional defined events to the event bus without code changes.

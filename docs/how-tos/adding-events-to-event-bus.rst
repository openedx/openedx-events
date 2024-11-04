Using the Open edX Event bus
============================

After creating a new Open edX Event, you might need to send it across services
instead of just within the same process. For this kind of use-cases, you might want
to use the Open edX Event Bus. Here, we list useful information about
adding a new event to the event bus:

- `How to start using the Event Bus`_


.. _How to start using the Event Bus: https://openedx.atlassian.net/wiki/spaces/AC/pages/3508699151/How+to+start+using+the+Event+Bus


Producing to event bus
^^^^^^^^^^^^^^^^^^^^^^

In the producing/host application, include ``openedx_events`` in ``INSTALLED_APPS`` settings and add ``EVENT_BUS_PRODUCER_CONFIG`` setting. For example, below snippet is to push ``XBLOCK_PUBLISHED`` to two different topics and ``XBLOCK_DELETED`` signal to one topic in event bus.

.. code-block:: python

   # .. setting_name: EVENT_BUS_PRODUCER_CONFIG
   # .. setting_default: {}
   # .. setting_description: Dictionary of event_types to dictionaries for topic-related configuration.
   #    Each topic configuration dictionary uses the topic as a key and contains:
   #    * A flag called `enabled` denoting whether the event will be published.
   #    * The `event_key_field` which is a period-delimited string path to event data field to use as event key.
   #    Note: The topic names should not include environment prefix as it will be dynamically added based on
   #    EVENT_BUS_TOPIC_PREFIX setting.
   EVENT_BUS_PRODUCER_CONFIG = {
       'org.openedx.content_authoring.xblock.published.v1': {
           'content-authoring-xblock-lifecycle': {'event_key_field': 'xblock_info.usage_key', 'enabled': True},
           'content-authoring-xblock-published': {'event_key_field': 'xblock_info.usage_key', 'enabled': True}
       },
       'org.openedx.content_authoring.xblock.deleted.v1': {
           'content-authoring-xblock-lifecycle': {'event_key_field': 'xblock_info.usage_key', 'enabled': True},
       },
   }

The ``EVENT_BUS_PRODUCER_CONFIG`` is read by openedx_events and a handler is
attached which does the leg work of reading the configuration again and pushing
to appropriate handlers.

11. Enable producing to event bus via settings
##############################################

Status
******

**Accepted**

Context
*******

In a previous ADR, we set the structure for the event bus publishing configuration to a dictionary like the following:

.. code-block:: python

    { 'org.openedx.content_authoring.xblock.published.v1': [
           {'topic': 'content-authoring-xblock-lifecycle', 'event_key_field': 'xblock_info.usage_key', 'enabled': True},
           {'topic': 'content-authoring-xblock-published', 'event_key_field': 'xblock_info.usage_key', 'enabled': False},
       ],
       'org.openedx.content_authoring.xblock.deleted.v1': [
           {'topic': 'content-authoring-xblock-lifecycle', 'event_key_field': 'xblock_info.usage_key', 'enabled': True},
       ],
   }

While attempting to implement this for edx-platform, we came across some problems with using this structure. In particular, it results in ambiguity
because maintainers can accidentally add something like
``{'topic': 'content-authoring-xblock-lifecycle', 'event_key_field': 'xblock_info.usage_key', 'enabled': True}`` and
``{'topic': 'content-authoring-xblock-lifecycle', 'event_key_field': 'xblock_info.usage_key', 'enabled': False}`` to the same event_type.
Also, as written, this configuration requires maintainers to copy over the entire configuration to override it, which is non-obvious
to people who may only be trying to enable/disable a single event while keeping everything else the same. Moreover, it's also non-obvious
that enabling/disabling an existing event/topic pair requires reaching into the structure, searching for the dictionary with the correct topic, and modifying
the existing object, which is awkward.

This ADR aims to propose a new structure that will provide greater flexibility in using this configuration.


Decision
********

The new EVENT_BUS_PRODUCER_CONFIG will have the following configuration format:

.. code-block:: python

   # .. setting_name: EVENT_BUS_PRODUCER_CONFIG
   # .. setting_default: {}
   # .. setting_description: Dictionary of event_types to dictionaries for topic related configuration.
   #    Each topic configuration dictionary uses the topic as a key and contains a flag called `enabled`
   #    denoting whether the event will be and `event_key_field` which is a period-delimited string path
   #    to event data field to use as event key.
   #    Note: The topic names should not include environment prefix as it will be dynamically added based on
   #    EVENT_BUS_TOPIC_PREFIX setting.
   EVENT_BUS_PRODUCER_CONFIG = {
       'org.openedx.content_authoring.xblock.published.v1': {
           'content-authoring-xblock-lifecycle': {'event_key_field': 'xblock_info.usage_key', 'enabled': False}
           'content-authoring-xblock-published': {'event_key_field': 'xblock_info.usage_key', 'enabled': True}
       },
       'org.openedx.content_authoring.xblock.deleted.v1': {
           'content-authoring-xblock-lifecycle': {'event_key_field': 'xblock_info.usage_key', 'enabled': True},
       },
   }

In edx-platform, it will be added to the KEYS_WITH_MERGED_VALUES list to allow partial additions/overrides.

Consequences
************

* As long as the implementing IDA has a concept of KEYS_WITH_MERGED_VALUES (more complex configurations that can be modified via code in settings),
maintainers can add existing topics to new event_types without having to recreate the whole dictionary
* There is no ambiguity about whether an event/topic pair is enabled or disabled

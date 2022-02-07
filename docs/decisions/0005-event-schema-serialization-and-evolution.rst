Event schema serialization and evolution
----------------------------------------


Status
~~~~~~

Provisional

Context
~~~~~~~


.. note:: Because the event definitions are shared, this decision applies to both external and internal events

Open edX is currently experimenting with event bus technology (`OEP-52: Event Bus <https://github.com/openedx/open-edx-proposals/pull/233>`_). The goal is to iterate through different implementations of an event bus and slowly get to a solution that works for the larger Open edX developer community.

Currently, the specification for an event are written as OpenEdxPublicSignal instances in signal.py modules in `openedx-events<https://github.com/eduNEXT/openedx-events/blob/main/openedx_events/learning/signals.py>`_ repository.

Over time, as needs change, applications will need the schema for an event to change.

For internal events, there is some discussion of versioning events related to how they might change in https://github.com/eduNEXT/openedx-events/blob/main/docs/decisions/0002-events-naming-and-versioning.rst. Schema for event bus messages is defined in openedx-events as signal classes.

However, for the event bus, we will be introducing more rigorous event evolution rules using an explicit schema and schema registry. We have decided to use Avro elsewhere (`OEP-52/decisions/001-schema-representation.rst<https://github.com/openedx/open-edx-proposals/pull/233/files#diff-70c71499189a23f546da507c5bfdc0fea674f4cbbc5c039298d8390d6930a5ca>`_).

Event schemas can evolve in various ways and each implementation of an event bus should choose a schema evolution configuration. The choices include how data can change, as well as the order in which producer and consumer needs to be deployed with new changes.

Event bus technologies support various schema evolutions::

- Backward / Backward Transitive: Allows you to delete fields and add optional fields. The consumer of the messages must upgrade to handle new schema before producer.

- Forward / Forward Transitive: Allows you to add fields and delete optional fields. The producer of the messages must upgrade to handle new schema before consumer of  messages.

- Full / Full Transitive: Allows you to add or delete optional fields. Either producer or consumer can change first.


Currently, the schema for event bus messages in defined through two classes: OpenEdxPublicSignal and attrs decorated classes in data.py modules (`example <https://github.com/eduNEXT/openedx-events/blob/main/openedx_events/learning/data.py>`_).

OpenEdxPublicSignal defines all the information necessary to create, serialize, and send an event. This includes the data to be sent and the metadata. The data to be sent is defined as the 'init_data' attribute. 'init_data' is a dict of key/value pairs. The keys are strings and the values can be of various types (the exact supported types has not be specified yet). These keys correspond to keyword arguments sent via the signal.

The attrs decorated classes (`example<https://github.com/eduNEXT/openedx-events/blob/main/openedx_events/learning/data.py>`_) are used to structure the data sent. Hopefully, most of the values in 'init_data' attribute in OpenEdxPublicSignal are of these attrs decorated classes.
Some helpful information about OpenEdxPublicSignal class:


Decision
~~~~~~~~

- The ability to add new data to an event definition is being prioritized over the ability to delete information. Deleting will not be allowed without introducing breaking changes.

- The top-level data dict of an OpenEdxPublicSignal can be evolved by adding new key/values. At this time, they will all be considered required.

- An attr Data class will not be evolved once in use. If new fields are required for an event, they can only be added into the top-level data dict.

- The above decisions result in a decision to use “Forward / Forward Transitive” schema evolution for external events. Although, it is possible to use “Full / Full Transitive” schema evolution and defer adjusting the rule until schema changes are required, or we add more flexibility.

Consequences
~~~~~~~~~~~~

- As noted in the decision, once events are evolved, we must use “Forward / Forward Transitive” with the event bus for external events. This means that the producer of an updated event must upgrade to handle the new schema before consumers can be upgraded.
- It is unclear what CI functionality can exist to catch schema changes that break the rules before the schema registry tests the rules for external events in some test environment.



Deferred/Rejected Decisions
~~~~~~~~~~~~~~~~~~~~~~

We could add the ability to add optional fields to an event, possibly into the attr Data classes and/or possibly into the top-level data dict in the OpenEdxPublicSignal.

- Optional fields would allow for “Full / Full Transitive” schema evolution. This option provides more flexibility around deployment of upgraded producers and consumers indepently, which is useful when each is owned by different teams.

- Optional fields would add additional complexity to the definitions, as well as to the bridge code that serializes these definitions for external events.

- Optional fields may enable cleaner event definitions in the case that new data would make more sense in the attr Data class than in the top-level data dict for all events that share the same Data class.

- Due to the complexity, this work is being deferred and this decision can be revisited when and if a valid use case arises.

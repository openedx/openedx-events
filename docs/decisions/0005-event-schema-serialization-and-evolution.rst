Event schema serialization and evolution
----------------------------------------


Status
~~~~~~

Provisional

Context
~~~~~~~

TODO: figure out what is note and what is context

Note: Because the event definitions are shared, this applies to both external and internal events
.. note:: Open edX is currently experimenting with event bus technology [point to OEP?]. The goal is to iterate through different implementations of an event bus and slowly get to a solution that works for the larger Open edX developer community.

Over time, as needs change, applications will need the schema for an event to change. Since the event definitions will be shared between internal and external events, changes to the event will affect both cases (internal and external).

For internal events, there is some discussion of versioning events related to how they might change in https://github.com/eduNEXT/openedx-events/blob/main/docs/decisions/0002-events-naming-and-versioning.rst. Schema for event bus messages is defined in openedx-events as signal classes.

However, for the event bus, we will be introducing more rigorous event evolution rules using an explicit schema and schema registry. We have decided to use Avro elsewhere (TODO point to ADR).

Using Avro, there are specific configurations for schema evolution, that affect how data can change, as well as the order in which producers and consumers need to be deployed to handle updated schemas. (TODO Point to doc for definitions.)


Event bus technologies support various schema evolutions::

- Backward / Backward Transitive: Allows you to delete fields and add optional fields. The consumer of the messages must upgrade to handle new schema before producer.

- Forward / Forward Transitive: Allows you to add fields and delete optional fields. The producer of the messages must upgrade to handle new schema before consumer of  messages.

- Full / Full Transitive: Allows you to add or delete optional fields. Either producer or consumer can change first.



At this time, the current implementation of the data inside the OpenEdxPublicSignal class is split into two parts:
There is a top-level data dict of key/value pairs. These keys correspond to keyword arguments sent via the signal.
There are also attr based Data classes. Some of the values in the top-level dict may include instances of these attr based Data classes.



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

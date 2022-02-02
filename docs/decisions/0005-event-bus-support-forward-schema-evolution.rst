1 Event Bus will aim to support Forward Schema evolution
--------------------------------------------------------

1.1 Context
~~~~~~~~~~~

- OpenedX is currently experimenting with event bus technology. The goal is to iterate through different implementations of event bus and slowly get to a solution that works for the larger OpenedX developer community.

- Schema for event bus messages is defined in openedx-events as signal classes.

- Over time, as needs change, applications will need the schema for an event to change.

- Event bus technologies support various schema evolutions.

  - Backward / Backward Transitive: Allows you to delete fields and add optional fields. The consumer of the messages must upgrade to handle new schema before producer.

  - Forward / Forward Transitive: Allows you to add fields and delete optional fields. The producer of the messages must upgrade to handle new schema before consumer of  messages.

  - Full / Full Transitive: Allows you to add or delete optional fields. Either producer or consumer can change first.

- Since this is the experimentation phase, the ease of adding new information will be prioritized higher than  deleting new information.

- Full schema evolution would be ideal, but it would add additional complexity to implementation.

1.2 Decision
~~~~~~~~~~~~

The initial implementation of OpenedX event bus will aim for Forward Transitive schema evolution.

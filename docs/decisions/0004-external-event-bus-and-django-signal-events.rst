External event bus and Django Signal events
-------------------------------------------

Status
~~~~~~

Provisional

1.1 Context
~~~~~~~~~~~

OpenedX services already use Django signals for internal events (`OEP-49: Django App Pattern <https://open-edx-proposals.readthedocs.io/en/latest/architectural-decisions/oep-0049-django-app-patterns.html#signals>`_). Additionally, we are adding the ability to trigger external events using an Event Bus(`OEP-52: Event Bus <https://github.com/openedx/open-edx-proposals/pull/233>`_).

This ADR concerns decisions made during trial of event bus regarding how external events will be triggered, and how external event bus builds off of decisions made for internal events.

This decision came out based on following conversations:

- `#38: What to send over the wire (Kafka)? <https://github.com/eduNEXT/openedx-events/issues/38>`_

- `#39: ARCHBOM-2010: How does Event Bus interact with OpenedX Django Signals? <https://github.com/eduNEXT/openedx-events/issues/39>`_

1.2 Decision
~~~~~~~~~~~~

- Event definitions (in the form of OpenEdxPublicSignal) will be shared between internal and external events.

- At this time, event bus events will be triggered from a Django signal handler of the Django signal representing the corresponding internal event.

- The Django signal must contain all event envelope and data to be sent across the event bus, such that it can be converted back into Django signals again on the consumer side.

- For consumption, the event bus implementation will convert the messages back into django signals and emit them within the consumer application.

Consequences
~~~~~~~~~~~~

- The OpenEdxPublicSignal serves as the event definition, and doubles as a Django signal.

- An external event will never be sent without a corresponding internal event (at this time, based on the current design).

- The external event bus handler will listen for relevant django signals (OpenEdxPublicSignals), and serialize them for the event bus (using AvroAttrsBridge [point to other ADR?]), and then send the messages over the wire.

- The use of the OpenEdxPublicSignal on both the event producing and event consuming sides for external events should hopefully provide a consistent mechanism to plug in for events.

- It is unclear whether the use of an extra layer of signals when sending/consuming external events will cause difficulties for implementations. If so, we may need to adjust and document when and where an alternative approach should be taken.

- The data definition in OpenEdxPublicSignal is geared toward signals, where the top-level dict represents keyword arguments emitted to the signal. This definition is not designed for event bus events, except in that it could be converted back to a signal.

Rejected Alternatives
~~~~~~~~~~~~~~~~

- Sending external event at same place of code as the internal Signal is sent. Decided that this is more complex than we need, and we can add this later if it becomes necessary.
- Sending external events without a corresponding internal event. This might be useful for Event Sourcing, and is not being ruled out forever, but is not currently being designed for.

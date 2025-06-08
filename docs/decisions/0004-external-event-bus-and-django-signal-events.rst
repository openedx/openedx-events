.. _ADR-4:

4. External event bus and Django Signal events
==============================================

Status
------

**Accepted**

Context
-------

Open edX services already use Django signals for internal events (see `OEP-50: Hooks extension framework <https://open-edx-proposals.readthedocs.io/en/latest/architectural-decisions/oep-0050-hooks-extension-framework.html>`_). Additionally, we are adding the ability to trigger external events using an Event Bus to the platform (see `OEP-52: Event Bus <https://github.com/openedx/open-edx-proposals/pull/233>`_).

The purpose of this ADR is to better define the relationship between the existing internal events and the new external events.

Decision
--------
Note that for purposes of this ADR, ``event`` refers to a dictionary of data that is emitted by a Django signal, specifically by an instance of ``OpenEdxPublicSignal``

- Event definitions will be shared between internal and external events. The event definitions will continue to be in the form of ``OpenEdxPublicSignal``, as decided in ADR ":doc:`0003-events-payload`".

- At this time, events will be published to the event bus from a Django signal handler. That is, when an internal event is sent via a Django signal, one of the handlers will take the event and publish it to the event bus.

- The Django signal must contain all of the necessary details to serialize events and send them across the event bus, such that they can be deserialized and sent by the same instance of ``OpenEdxPublicSignal`` again on the consumer side.

- For consumption, the event bus implementation will look up the correct ``OpenEdxPublicSignal`` from the deserialized event metadata and use it to emit the deserialized event within the consumer application.

Consequences
------------

- The ``OpenEdxPublicSignal`` serves as the event definition, and doubles as a Django signal, for both internal and external events. In other words, an instance of ``OpenEdxPublicSignal`` provides the schema for the events it can emit

- An external event will never be sent without a corresponding internal event (at this time, based on the current design).

- The external event bus handler will listen for Django signals (``OpenEdxPublicSignals``) that have been configured to be sent as external events. These external events will be serialized using utilities in this library, as decided in ADR ":doc:`0005-external-event-schema-format`", before sending the messages over the wire.

- The use of the ``OpenEdxPublicSignal`` on both the event producing and event consuming sides for external events should hopefully provide a consistent mechanism to plug in for events.

- It is unclear whether the use of an extra layer of signals when sending/consuming external events will cause difficulties for implementations. If so, we may need to adjust and document when and where an alternative approach should be taken.

Rejected Alternatives
---------------------

- Sending external event at same place of code as the internal event is sent. Decided that this is more complex than we need, and we can add this later if it becomes necessary.

- Sending external events without a corresponding internal event. This might be useful for event sourcing, and is not being ruled out forever, but is not currently being designed for.

Additional Resources
--------------------

If you want further background for this decision, see the following discussions:

- `#38: What to send over the wire (Kafka)? <https://github.com/openedx/openedx-events/issues/38>`_

- `#39: ARCHBOM-2010: How does Event Bus interact with OpenedX Django Signals? <https://github.com/openedx/openedx-events/issues/39>`_

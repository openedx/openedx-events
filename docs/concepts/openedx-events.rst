Open edX Events
===============

In the context of Open edX, events provide a mechanism for extending the platform
by enabling developers to listen to specific Django signals emitted by various
services and respond accordingly. This allows for customized reactions to key
actions or changes within the platform, without requiring direct modifications
to the Open edX platform codebase.

What are Open edX Events?
-------------------------

An Open edX Event is a Open edX specific Django signal that is emitted by a service
when a specific action or event occurs. These signals are used to notify other
services or components of the platform that an event has taken place, allowing them
to respond accordingly. Events are defined using the ``OpenEdxPublicSignal`` class,
which provides a structured way to define the data and metadata associated with
the event along with other relevant information.

Why are Open edX Events important?
----------------------------------

Open edX Events are a key component of the Hooks Extension Framework, which allows
developers to extend the functionality of the platform in a stable and maintainable
way. By triggering events for specific actions or changes within the platform, developers
can create event handlers that respond to these events and perform additional
actions or processing as needed. This enables a wide range of use cases, from
integrating with external systems to implementing custom business logic.

How are Open edX Events used?
-----------------------------

Developers can create handlers for Open edX Events by implementing Django signal
handlers that respond to specific events emitted by the platform. These signal
handlers can be registered using Django's signal mechanism, allowing them to
listen for events and execute custom logic in response. By defining events and
handlers in this way, developers can create modular, reusable components that
extend the functionality of the platform without requiring direct modifications
to the core codebase.

How do Open edX Events work?
----------------------------

Open edX Events are implemented using Django signals, which provide a way to
send and receive notifications within a Django application. Due to this design,
Open edX Events closely follow the Django signal pattern, allowing developers to
leverage their existing knowledge of Django signals.

The lifecycle of an Open edX Event can be summarized as follows:

1. A service emits an Open edX Event (Open edX specific Django signal) triggered by a specific action or event. The event data includes information about the event, such as the event name, timestamp, and any additional metadata.
2. Registered signal handlers listening for the event are called in response to the signal being emitted.
3. The signal handler performs additional processing or trigger other actions based on the event data.
4. The event is considered complete once all registered signal handlers have executed.

Here is an example of how that might look like with an existing event:

1. A user enrolls in a course, `triggering the COURSE_ENROLLMENT_CREATED event`_. This event includes information about the user, course, and enrollment details.
2. A `signal handler listening`_ for the ``COURSE_ENROLLMENT_CREATED`` event is called and processes the event data.
3. The signal handler sends a notification to the user confirming their enrollment in the course.
4. The event is considered complete once the signal handler has finished processing the event.

For a more detailed explanation of how Django signals work, refer to the `Django Signals Documentation`_.

For more details on the following topics, see the corresponding links:

- `Hooks Extension Framework`_: Overview of the Hooks Extension Framework.
- `Open edX Events Naming and Versioning`_: ADR defining the rules for naming and versioning Open edX Events.
- `Open edX Events Payload`_: ADR defining the payload structure for Open edX Events.
- `External Event Bus and Django Signal Events`_: ADR defining the relationship between internal and external events.

.. _Hooks Extension Framework: https://open-edx-proposals.readthedocs.io/en/latest/oep-0050-hooks-extension-framework.html
.. _Django Signals Documentation: https://docs.djangoproject.com/en/4.2/topics/signals/
.. _triggering the COURSE_ENROLLMENT_CREATED event: https://github.com/openedx/edx-platform/blob/master/common/djangoapps/student/models/course_enrollment.py#L777-L795
.. _signal handler listening: https://github.com/openedx/edx-platform/blob/master/common/djangoapps/student/models/course_enrollment.py#L777-L795
.. _Open edX Events Naming and Versioning: https://github.com/openedx/openedx-events/blob/main/docs/decisions/0002-events-naming-and-versioning.rst
.. _Open edX Events Payload: https://github.com/openedx/openedx-events/blob/main/docs/decisions/0003-events-payload.rst
.. _External Event Bus and Django Signal Events: https://github.com/openedx/openedx-events/blob/main/docs/decisions/0004-external-event-bus-and-django-signal-events.rst

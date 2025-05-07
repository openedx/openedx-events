Open edX Events Glossary
##########################

An event has multiple components that are used to define, trigger, and handle the event. This glossary provides definitions for some of the terms to ease the adoption of the Open edX Events library.

.. glossary::

    Event Receiver
      An event receiver, handler, or listener is a function that listens for a specific event and executes custom logic in response to the event being triggered. Since Events are Django-signals, then receivers are registered with the signal dispatcher and are called when the event is emitted. In Django, event receivers are known as signal receivers. Both terms can be used interchangeably. E.g., a receiver that listens for the ``COURSE_ENROLLMENT_CREATED`` event and creates a notification preference for the user.

    Event Trigger
      An event trigger is the action that causes an event to be emitted. When a trigger action occurs, the associated event is emitted, and any registered event receivers are called to handle the event. For example, when a user enrolls in a course, the ``COURSE_ENROLLMENT_CREATED`` event is triggered. In this case, the event trigger is the user enrolling in the course.

    Event Payload
      The event payload is the data associated with an event that is passed to event receivers when it's triggered. The payload of an event are data attribute classes (e.g. ``CourseEnrollmentData``, ``UserData``, etc.) that carry data about the event such as the event name, timestamp, and any additional metadata and information about the actual event. For more information, see the `Events Payload ADR`_.

    Event Type
      The event type is a unique identifier for an event that distinguishes it from other events. For example, ``org.openedx.content_authoring.xblock.published.v1``. The event type is used to identify the event, its purpose, and version. In the event bus context, the event type is used to connect events to the appropriate topics in the ``EVENT_BUS_PRODUCER_CONFIG``. E.g., the event type ``org.openedx.learning.course.enrollment.created.v1`` is used to identify the ``COURSE_ENROLLMENT_CREATED`` event.

    Event Definition
      An event is a signal that is emitted when a specific action occurs in the platform. The event definition is the instantiation of the ``OpenEdxPublicSignal`` class that defines the structure and metadata of an event. This definition includes information such as the event name, description, payload, and version. Event definitions are used to create events which are later imported into the services and are triggered by using the ``send_event`` method.

    Event Bus
      To be added soon.

    Event Bus Producer
      To be added soon.

    Event Bus Consumer
      To be added soon.

    Event Bus Topic
      To be added soon.

    Event Bus Producer Config
      To be added soon.

    Event Bus Settings
      To be added soon.

.. _Events Payload ADR: :doc: `/decisions/0003-events-payload`

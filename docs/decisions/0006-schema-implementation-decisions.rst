1 Schema Implementation decisions
---------------------------------

1.1 Context
~~~~~~~~~~~

This decision builds on and somewhat restates some of the decisions in following ADRs:

- `0003-events-payload.rst`_: Defines event structure.

- `0004-event-bus-as-extension-of-django-signals.rst`_: Defines event bus in relation to Django Signals.

- `0005-event-bus-support-forward-schema-evolution.rst`_: Defines current schema evolution compatibility for OpenedX event bus endeavor.

.. _0003-events-payload.rst: https://github.com/eduNEXT/openedx-events/blob/main/docs/decisions/0003-events-payload.rst
.. _0004-event-bus-as-extension-of-django-signals.rst: https://github.com/eduNEXT/openedx-events/blob/main/docs/decisions/0004-event-bus-as-extension-of-django-signals.rst
.. _0005-event-bus-support-forward-schema-evolution.rst: https://github.com/eduNEXT/openedx-events/blob/main/docs/decisions/0005-event-bus-support-forward-schema-evolution.rst

And this decision is a result of following conversations:
- `#38: What to send over the wire (Kafka)? <https://github.com/eduNEXT/openedx-events/issues/38>`_

- `#39: ARCHBOM-2010: How does Event Bus interact with OpenedX Django Signals? <https://github.com/eduNEXT/openedx-events/issues/39>`_

1.2 Decision
~~~~~~~~~~~~

-  Since the external event bus is an extension of Django signals as stated in  `0004-event-bus-as-extension-of-django-signals.rst`_, it will use the event message payload method specified in  `0003-events-payload.rst`_. OpenEdxPublicSignal classes will define the schema for event bus messages

  - All the data to be sent over the message bus will be sent as a dict. This dict will be passed to OpenEdxPublicSignal class as the "data" keyword.

      - The keys in the data will be strings

      - The values can be: python primitives(int, str, dict, list ...), attrs decorated classes defined in openedx-events repository, or custom classes that have extensions defined in AvroAttrsBridge class.

        - Ideally, the values are attrs decorated classes, other types are supported for convenience.

  - The metadata (topic name, version information) for an event will be defined as attributes in signal class. If is unclear exactly what metadata will be needed.

  - Example signal class:

    .. code:: python

        from openedx_events.tooling import OpenEdxPublicSignal
        from openedx_events.learning.data import CourseEnrollmentData

        COURSE_ENROLLMENT_CHANGED = OpenEdxPublicSignal(
            event_type="org.openedx.learning.course.enrollment.changed.v1",  # metadata
            data={   # "data" attribute
                "enrollment": CourseEnrollmentData, # keyword in "data" attribute
            }
        )

- If you need to add more information to a message, add it as an additional field in “data” dict in your signal class.

- Once a keyword has been added to “data” dict, it will be required for all new messages.

- Once an attrs decorated class is defined in openedx-events, it should not change. New information should be added as a keyword in “data” attribute.

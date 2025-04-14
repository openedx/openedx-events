16. Event Design Best Practices
###############################

Status
------

**Accepted**

Context
-------

It is important to follow standards to ensure that the events are consistent, maintainable, and reusable. The design of the events should be self-descriptive, self-contained, and provide enough information for consumers to understand the message. This ADR aims to provide a set of suggested practices for designing Open edX events.

Decision
--------

We have compiled a list of suggested practices taken from the following sources:

- `Event-Driven Microservices`_
- `Event-Driven article`_
- `Thin Events - The lean muscle of event-driven architecture`_

These are the practices that we recommend reviewing and following when designing an Open edX Event and contributing to the library. The goal is to implement events that are consistent with the architecture, reusable, and maintainable over time.

Event Purpose and Content
~~~~~~~~~~~~~~~~~~~~~~~~~

- An event should describe as accurately as possible what happened (what) and why it happened (why). It must contain enough information for consumers to understand the message. For instance, if an event is about a user enrollment, it should contain the user's data, the course data, and the enrollment status and the event should be named accordingly.
- Avoid immediately contacting the source service to retrieve additional information from the consumer-side. Instead, consider adding the necessary information to the event payload by managing the granularity of the event. If the event requires additional information, consider adding a field to the event that contains the necessary information. This will reduce the number of dependencies between services and make the event more self-contained.
- Keep the event size small. Avoid adding unnecessary information to the event. If the information is not necessary for consumers to react to the event, consider removing it.
- Avoid adding flow-control information or business logic to events. Events should be solely a representation of what took place. If a field is necessary to control the behavior of the consumer, consider moving it to the consumer side. If adding additional data to the event is absolutely necessary document the reasoning behind it and carefully study the use case and implications.

Here is an example of an event that follows these practices which is emitted when the a user registers:

.. code-block:: python

    # Location openedx_events/learning/signal.py
    # .. event_type: org.openedx.learning.student.registration.completed.v1
    # .. event_name: STUDENT_REGISTRATION_COMPLETED
    # .. event_description: emitted when the user registration process in the LMS is completed.
    # .. event_data: UserData
    STUDENT_REGISTRATION_COMPLETED = OpenEdxPublicSignal(
        event_type="org.openedx.learning.student.registration.completed.v1",
        data={
            "user": UserData,
        }
    )

Where:

- The event name indicates what happened: ``STUDENT_REGISTRATION_COMPLETED``.
- The event description explains why the event happened: ``emitted when the user registration process in the LMS is completed``.
- The event data contains data directly related to what happened ``UserData`` which should contain the necessary information to understand the event, like the username and email of the user.

Responsibility and Granularity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Design events with a single responsibility in mind. Each event should represent a single action or fact that happened in the system. If an event contains multiple actions, consider splitting it into multiple events. For instance, if the course grade is updated to pass or fail, there should be two events: one for the pass action and another for the fail action.

.. note:: For the :doc:`Event Bus <../concepts/event-bus>`, events that are split across multiple actions are an exceptional case where the same event :term:`Topic` should be used to help maintain order across these events.

- Manage the granularity of the event so it is not too coarse (generic with too much information) or too fine-grained (specific with too little information). When making a decision on the granularity of the event, start with the minimum required information for consumers to react to the event and add more information as needed with enough justification. If necessary, leverage API calls from the consumer side to retrieve additional information but always consider the trade-offs of adding dependencies with other services.
- Ensure that the triggering logic is consistent and narrow. For instance, if an event is triggered when a user enrolls in a course, it should be triggered when the user enrolls in a course in all ways possible to enroll in a course. If the event is triggered when a user enrolls in a course through the API, it should also be triggered when the user enrolls in a course through the UI.

For instance, consider the following events:

.. code-block:: python

    # Location openedx_events/learning/signal.py
    # .. event_type: org.openedx.learning.course.grade.passed.v1
    # .. event_name: COURSE_GRADE_PASSED
    # .. event_description: emitted when the user's course grade is updated to pass.
    # .. event_data: CourseGradeData
    COURSE_GRADE_PASSED = OpenEdxPublicSignal(
        event_type="org.openedx.learning.course.grade.passed.v1",
        data={
            "grade": CourseGradeData,
        }
    )

    # Location openedx_events/learning/signal.py
    # .. event_type: org.openedx.learning.course.grade.failed.v1
    # .. event_name: COURSE_GRADE_FAILED
    # .. event_description: emitted when the user's course grade is updated to fail.
    # .. event_data: CourseGradeData
    COURSE_GRADE_FAILED = OpenEdxPublicSignal(
        event_type="org.openedx.learning.course.grade.failed.v1",
        data={
            "grade": CourseGradeData,
        }
    )

Where:

- The event name indicates what happened: ``COURSE_GRADE_PASSED`` and ``COURSE_GRADE_FAILED``.
- The event description explains why the event happened: ``emitted when the user's course grade is updated to pass`` and ``emitted when the user's course grade is updated to fail``.
- The event data contains data directly related to what happened ``CourseGradeData`` which should contain the necessary information to understand the event, like the user, the course, the grade, and the date of the grade update.
- The granularity of the event is managed by having two events: one for the pass action and another for the fail action.

Each of these practices should be reviewed with each case, and the granularity of the event should be adjusted according to the use case and the information required by the consumers.

Event Structure and Clarity
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Use appropriate data types and formats for the event fields. Don't use generic data types like strings for all fields. Use specific data types like integers, floats, dates, or custom types when necessary.
- Avoid ambiguous data fields or fields with multiple meaning. For instance, if an event contains a field called ``status`` it should be clear what the status represents. If the status can have multiple meanings, consider splitting the event into multiple events or adding a new field to clarify the status.

For instance, consider the ``CourseEnrollmentData`` class:

- The ``mode`` field is a string that represents the course mode. It could be a string like "verified", "audit", "honor", etc.
- The ``is_active`` field is a boolean that represents whether the enrollment is active or not.
- The ``creation_date`` field is a datetime that represents the creation date of the enrollment.
- The ``created_by`` field is a ``UserData`` that represents the user who created the enrollment.
- The ``user`` field is a ``UserData`` that represents the user associated with the Course Enrollment.
- The ``course`` field is a ``CourseData`` that represents the course where the user is enrolled in.

Consumer-Centric Design
~~~~~~~~~~~~~~~~~~~~~~~

- When designing an event, consider the consumers that will be using it. What information do they need to react to the event? What data is necessary for them to process the event?
- You can't always predict the needs of consumers in the future. Ensure your design is discrete, flexible, and well-documented, so new and novel use cases can be developed.
- Design events carefully from the start to minimize breaking changes for consumers, although it is not always possible to avoid breaking changes.

Some of these practices might not be applicable to all events, but they are a good starting point to ensure that the events are consistent and maintainable over time. So, design the event so it is small, well-defined and only contain relevant information.

In addition to these practices, review the Architectural Decision Records (ADRs) related to events to understand the naming, versioning, payload, and other practices that are specific to Open edX events.

Consequences
------------

Following these practices will help ensure that the events are consistent, maintainable, and reusable. It will also help consumers understand the message and react to the event accordingly. However, it might require additional effort to design the event and ensure that it contains the necessary information for consumers to react to the event, although this effort will pay off in the long run. Having these standards in place will also make the decision process easier when designing new events.

.. _Event-Driven Microservices: https://www.oreilly.com/library/view/building-event-driven-microservices/9781492057888/
.. _Event-Driven article: https://martinfowler.com/articles/201701-event-driven.html
.. _Thin Events - The lean muscle of event-driven architecture: https://www.thoughtworks.com/insights/blog/architecture/thin-events-the-lean-muscle-of-event-driven-architecture

16. Event Design Practices
###########################

Status
------

Draft

Context
-------

It is important to follow standards to ensure that the events are consistent, maintainable, and reusable. The design of the events should be self-descriptive, self-contained, and provide enough information for consumers to understand the message. This ADR aims to provide a set of suggested practices for designing Open edX events.

Decision
--------

We have compiled a list of suggested practices taken from `Event-Driven Microservices`_ and the `Event-Driven article`_ that we recommend reviewing and following when designing an Open edX Event and contributing to the library. The goal is to implement events that are consistent with the architecture, reusable, and maintainable over time.

#. An event should describe as accurately as possible what happened (what) and why it happened (why). It must contain enough information for consumers to understand the message. For instance, if an event is about a user enrollment, it should contain the user's data, the course data, and the enrollment status and the event should be named accordingly.
#. Design events to be self-descriptive and self-contained. The event should contain all the information necessary about what took place for consumers to react to the event without consulting other data sources.
#. Ensure the event carries all necessary data to prevent runtime dependencies with other services. An event doesn't need to contain all the data of the entities involved, but it should contain enough information for consumers to not immediately need to query other services to understand what took place. This might be not always possible, but it is good to keep in mind to decrease the coupling between services.
#. Avoid adding flow-control information or business logic to events. Events should be solely a representation of what took place. If a field is necessary to control the behavior of the consumer, consider moving it to the consumer side.
#. Use appropriate data types and formats for the event fields. Don't use generic data types like strings for all fields. Use specific data types like integers, floats, dates, or custom types when necessary.
#. Avoid ambiguous data fields or fields with multiple meaning. For instance, if an event contains a field called ``status`` it should be clear what the status represents. If the status can have multiple meanings, consider splitting the event into multiple events or adding a new field to clarify the status.
#. Design events with a single responsibility in mind. Each event should represent a single action or fact that happened in the system. If an event contains multiple actions, consider splitting it into multiple events. For instance, if the course grade is updated to pass or fail, there should be two events: one for the pass action and another for the fail action.
#. Manage the granularity of the event so it is not too coarse (generic name with too much information) or too fine-grained (specific name with too little information). It should be expressive enough to be useful.
#. When designing an event, consider the consumers that will be using it. What information do they need to react to the event? What data is necessary for them to process the event?
#. Design events carefully to minimize breaking changes for consumers.

Some of these practices might not be applicable to all events, but they are a good starting point to ensure that the events are consistent and maintainable over time. So, design the event so it is small, well-defined and only contain relevant information.

In addition to these practices, review the Architectural Decision Records (ADRs) related to events to understand the naming, versioning, payload, and other practices that are specific to Open edX events.

.. _Event-Driven Microservices: https://www.oreilly.com/library/view/building-event-driven-microservices/9781492057888/
.. _Event-Driven article: https://martinfowler.com/articles/201701-event-driven.html

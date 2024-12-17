Event Design Practices
######################

Status
------

Proposed

Context
-------

It is important to follow standards to ensure that the events are consistent, maintainable, and reusable. The design of the events should be self-descriptive, self-contained, and provide enough information for consumers to understand the message. This ADR aims to provide a set of suggested practices for designing Open edX events that are consistent with the architecture and contribute to the overall quality of the Open edX ecosystem.

Decision
--------

We have compiled a list of suggested practices taken from `Event-Driven Microservices`_ and the `Event-Driven article`_ that we recommend reviewing and following when designing an Open edX Event and contributing to the library. The goal is to implement events that are consistent with the architecture, reusable, and maintainable over time.

#. An event should describe as accurately as possible what happened (what) with its and why it happened (why). It must contain enough information for consumers to understand the message.
#. Design events to be self-descriptive and self-contained. It should contain all the information necessary about what took place for consumers to react to the event without consulting other data sources.
#. Avoid ambiguous data fields or fields with multiple meaning.
#. Design events with a single responsibility in mind. Each event should represent a single action or fact.
#. Avoid adding flow-control information or business logic to events. Events should be solely a representation of what happened.
#. Use appropriate data types and formats for the event fields.
#. Design the event so it is small, well-defined and only contain relevant information. Avoid including unnecessary or unrelated context.
#. Ensure the event carries all necessary data to prevent runtime dependencies with other services.
#. Manage the granularity of the event so it is not too course (generic name with too much information) or too fine-grained (specific name with too little information). It should be expressive enough to be useful.
#. When designing an event, consider the consumers that will be using it. What information do they need to react to the event? What data is necessary for them to process the event?

Some of these practices might not be applicable to all events, but they are a good starting point to ensure that the events are consistent and maintainable over time.

.. _Event-Driven Microservices: https://www.oreilly.com/library/view/building-event-driven-microservices/9781492057888/
.. _Event-Driven article: https://martinfowler.com/articles/201701-event-driven.html

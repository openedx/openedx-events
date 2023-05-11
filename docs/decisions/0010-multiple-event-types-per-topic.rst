10. Multiple event types per topic
##################################

Status
******

- **Accepted** DATE TO BE ADDED BEFORE MERGING

Context
*******

For the initial implementation of the event bus, we decided to limit each topic to use a single schema. This meant that every signal in openedx-events required a different topic. This worked for our initial use case, course catalog updates, because all changes were considered updates and could be emitted using the same signal.
However, other types of events are not so easily grouped into a single signal. For example, there are different signals for ``XBLOCK_PUBLISHED``, ``XBLOCK_UPDATED``, and ``XBLOCK_DUPLICATED``, and indeed different schemas across the three signals. Routing these signals through different topics could lead to events being processed in a nonsensical order, for example an xblock being duplicated before it's been published. See `Should You Put Several Event Types in the Same Kafka Topic?`_ and `Putting Several Event Types in the Same Topic – Revisited`_ for more information on why it can be useful to group different event types on the same topic.

.. _Should You Put Several Event Types in the Same Kafka Topic?: https://www.confluent.io/blog/put-several-event-types-kafka-topic/
.. _Putting Several Event Types in the Same Topic – Revisited: https://www.confluent.io/blog/multiple-event-types-in-the-same-kafka-topic/

Decision
********
All implementations of the event bus must support sending multiple event types to a single topic.

Note that here, "topic" refers to however the event bus implementation groups related events (for example, streams in Redis).

Consequences
************
* Event consumers will need to determine the signal from the message headers rather than taking a signal as a passed argument in the management command.

Rejected Alternatives
*********************

Require related event types to have the same schema
===================================================
In theory we could avoid the issue of event types with different schemas on the same topic by simply not allowing them, requiring all event types that are intended to go on the same topic to have the same schema. This would require knowing in advance which event types will go to which topics and likely result in lots of extraneous fields which are only necessary for some of the event types and not others. This is very much an anti-pattern.

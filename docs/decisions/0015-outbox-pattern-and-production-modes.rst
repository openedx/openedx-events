15. Outbox pattern and production modes
#######################################

Status
******

**Provisional**

Context
*******

.. note::
  Clarification on language: We use "publish", "produce", and "send" somewhat interchangeably in various places in our code and documentation to refer to the transmission of an event from an IDA to the Event Bus message broker. The term "send" is also used in reference to the Django signal system. In this ADR, "send" will refer only to sending to an OpenEdxPublicSignal Django signal, and "publish" will be used for transmitting an event to the message broker.

Some of the event types in the Event Bus might be more sensitive than others to dropped, duplicated, or reordered events. The message broker itself is partially responsible for ensuring that these problems do not occur in transit, but we also need to ensure that the handoff of events to the broker is reliable.

These are the properties we wish to ensure in the general case:

- **Atomicity**: Many events are related to data that is written to the database in the same request, but transactions can either commit or abort. This gives us two sub-properties:

  - **Atomic success**: When a transaction successfully commits in the IDA, any created events relating to that data are durably published to the message broker. This is more important for events intended to keep services synchronized (publishing "latest state of entity" events), and may be less important for some kinds of notification events (especially anything used for tracking or statistics).
  - **Atomic failure**: When a transaction fails, due to a rollback, network interruption, or application crash, no events related to those database writes are published to the message broker. Otherwise, these events would be "counterfactuals" that misrepresent the publishing service's internal state. This could result in strange behavior such as incorrect notifications to users, and potentially could produce security issues.

- **Ordering**: If multiple events are published to the same topic, their ordering is preserved. This raises the question of "ordered according to what metric", as concurrency is in play, so the nature of this property may vary by event.

This is only in the general case, as some events may not be connected to database transactions, some consumers might tolerate violations of either atomic success or failure, and not all events may have strict notions of ordering. However, in the general case violations of any of these can result in consistency failures between services that might not be corrected over any time scale.

It's also worth noting a goal we don't have, that of avoiding duplication. At-least-once delivery is acceptable; exactly-once delivery is not required. Double-publishing of events is permissible as long as this only happens occasionally (for performance reasons) and does not entail a violation of ordering.

As of 2023-11-09 we publish events in two different ways relative to transactions:

- **Immediate publish**: The event is published to the event bus immediately upon the signal being sent, which will generally occur inside Django's request-level transaction (if using ``ATOMIC_REQUESTS``). This preserves atomicity in the success case as long as the broker is reachable, even if the IDA crashes -- but it does not preserve atomicity when the transaction fails. There is also no ordering guarantee in the case of concurrent requests.
- **On-commit publish**: The event is published from a ``django.db.transaction.on_commit`` callback. This preserves atomicity in the failure case, but the IDA could crash after transaction commit but before calling the broker -- or more commonly, the broker could be down or unreachable, and all of the on-commit-published events would be lost during that interval. Ordering is also not preserved here.

We currently use an ad-hoc mix of immediate and on-commit publish in edx-platform, depending on how code sends to particular OpenEdxPublicSignals. For example, the code path for ``COURSE_CATALOG_INFO_CHANGED`` involves an explicit call to ``django.db.transaction.on_commit`` in order to ensure an on-commit publish is used. But most signal sends do not have any such call, and are likely published immediately. This uncontrolled state reflects our iterative approach to the event bus as well as our choice to start with events that are backed by other synchronization measures which can correct for consistency issues. However, we'd like to start handling events that require stronger reliability guarantees, such as those in the ecommerce space.

Decision
********

We will implement the transactional outbox pattern (or just "outbox pattern") in order to allow binding event publishing to database transactions. Events will default to on-commit publish, but openedx-events configuration will be enhanced to allow configuring each event to a choice of **publishing mode** (on-commit or outbox).

In the outbox pattern, events are not published as part of the request/response cycle, but are instead appended to an "outbox" database table within the transaction. A worker process operating in a separate transaction works through the list in order, publishing them to the message broker and removing them once the broker has acknowledged them. This is the standard solution to the dual-write problem and is likely the only way to meet all of the criteria. Atomicity is ensured by bringing the *intent* to publish an event into the transaction's ACID guarantees. Transaction commits also impose a meaningful ordering across all hosts using the same database. Even events that are not otherwise published in a transactional context will benefit from the at-least-once delivery semantics.

openedx-events will change to support two modes for publishing events when an OpenEdxPublicSignal's ``send_event(...)`` is called:

- ``on-commit``: Delay publishing to the event bus until after the current transaction commits, or immediately if there is no open transaction (as might occur in a worker process).

  - Atomicity is preserved in the success case, but not in the failure case. (Events published in this mode may occasionally be lost, but should never be sent when a transaction fails.)
  - This does not necessarily preserve ordering of events across multiple hosts.

- ``outbox``: Prep the signal for publishing, and save in an outbox table for publishing as soon as possible. A worker process will then relay events from the outbox to the broker and mark them as successfully published. Another management command will be needed to periodically purge old processed events.

  - Atomicity is fully preserved.
  - As long as only a single worker per topic is emptying the outbox, ordering of events can be fully maintained.

openedx-events will add a per event type configuration field specifying the event’s publishing mode in the form of a new key-topic field inside ``EVENT_BUS_PRODUCER_CONFIG``. It will also add a new Django setting ``EVENT_BUS_PRODUCER_MODE`` that names a mode to use when not otherwise specified (defaulting to ``on-commit``.)

This will remove the ability to publish an event immediately, as none of the currently implemented events would benefit from it. If in the future there is an event type that requires it, perhaps because it represents a request or attempt or even a failure, an ``immediate`` mode can be added.

Implementation Plan
===================

(Details in this section are subject to change.)

The most promising option for implementing the transactional outbox is `django-jaiminho`_, a Django app that manages adding to and emptying an outbox table. ``django-jaiminho`` would be added as a dependency of openedx-events and to the ``INSTALLED_APPS`` of event-producing IDAs, and several long-running workers running jaiminho management commands would be required for each event-producing IDA.

Unknowns and future decisions:

- Format for the event data in the outbox. No further event-specific DB queries should be required for creating the bytestring for the wire format, but it should not be serialized in a way that is specific to Kafka, Redis, etc.
- Safeguards around inadvertently changing the save-to-outbox function's name and module, since those are included in jaiminho's outbox records.
- Observability of outbox size and event publish errors.

.. _django-jaiminho: https://github.com/loadsmart/django-jaiminho

Consequences
************

- The event bus becomes far more reliable, and able to handle events that require at-least-once delivery. The need for manual re-publishing of events should become very rare.
- The new outbox functionality, if used, comes with operational complexity. Adding a new worker process to every service that publishes events will further increase the orchestration needs of Open edX. (See alternatives section for a possible workaround.)
- Duplication becomes possible, so we would need a way to avoid publishing the same event over and over again to the broker if the broker is failing to return acknowledgments. We may need to revisit existing events and improve documentation around ensuring that consumers can tolerate duplication, either by ensuring that events are idempotent or by keeping track of which event IDs have already been processed.
- The database will be required to store an unbounded number of events during a broker outage, worker outage, or event bus misconfiguration.

Some events are currently published on-commit because the signal ``send_event()`` call is made in a ``transaction.on_commit()`` callback. ``emit_catalog_info_changed_signal`` is a known example of this. These would need to be migrated to use the new on-commit publishing mode and to lift the signal send out of the on_commit callback, calling send_event directly instead.

Rejected and Unplanned Alternatives
***********************************

Change Data Capture
===================

Change data capture (CDC) is a method of directly streaming database changes from one place to another by following the DB's transaction log. This provides the same transactionality benefits as the outbox method. `Debezium <https://debezium.io/>`_ is an example of such a system and can read directly from the database and publish to Kafka, where the data can then be transformed and routed to other systems. While a CDC platform could publish data to the Open edX event bus, it would also be redundant with the event bus. In the example of Debezium, a deployment would still need a Kafka cluster even if they wanted to put event data into Redis.

CDC systems also source their data at a lower level than we're targeting with the event bus; Django usually insulates us from schema details via an ORM layer, but CDC involves reading table data directly. We'd have tight coupling with our DB schemas. And the eventing system we've chosen to build operates at a higher abstraction layer than database writes, creating another conceptual mismatch. Theoretically, a CDC system could also be responsible for reading events from an outbox, allowing high-level eventing, but this is unlikely to be more palatable than just running a management command in a loop.

Non-worker event publishing
===========================

The outbox pattern usually involves running a worker process that handles moving data from the outbox to the broker. However, it may be possible for deployers to avoid this with the use of some alternative middleware. For example, a custom middleware could flush events to the broker at the end of each event-producing request. The middleware's ``post_response`` would run outside of the request's main transaction. It would check if the request had created events, and if so, it would pull *at least that many* events from the outbox and publish them to the broker, then remove them from the outbox. If the server crashed before this could complete, later requests would eventually complete the work. This would also cover events published by workers and other non-request-based processes.

Web requests that result in events being published would have higher response latency, as they would have to finish an additional DB read, broker call, and DB write before returning the response to the user. Event latency would also increase and become more variable due to the opportunistic approach.

It's also conceivable that each Django server in the IDA could start a background process to act as an outbox-emptying worker.

We're not planning on implementing either of these, but they should be drop-in replacements for the long-running management command, and could be developed in the future by deployers who need such an arrangement.

References
**********

- Microservices.io on the transactional outbox pattern: https://microservices.io/patterns/data/transactional-outbox.html
- An introduction to jaiminho: https://engineering.loadsmart.com/blog/introducing-jaiminho

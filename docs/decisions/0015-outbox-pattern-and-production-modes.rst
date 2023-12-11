15. Outbox pattern and production modes
#######################################

Status
******

**Provisional**

Context
*******

Some of the event types in the Event Bus might be more sensitive than others to dropped, duplicated, or reordered events. The message broker itself is partially responsible for ensuring that these problems do not occur in transit, but we also need to ensure that the handoff of events to the broker is reliable.

These are the properties we wish to ensure in the general case:

- **Atomicity**: Many events are related to data that is written to the database in the same request, but transactions can either commit or abort. This gives us two sub-properties:

  - **Atomic success**: When a transaction successfully commits in the IDA, any produced events relating to that data are durably transmitted to the message broker. This is more important for events intended to keep services synchronized (sending "latest state of entity" events), and may be less important for some kinds of notification events (especially anything used for tracking or statistics).
  - **Atomic failure**: When a transaction fails, due to a rollback, network interruption, or application crash, no events related to those database writes are sent to the message broker. Otherwise, these events would be "counterfactuals" that misrepresent the producing service's internal state. This could result in strange behavior such as incorrect notifications to users, and potentially could produce security issues.

- **Ordering**: If multiple events are produced to the same topic, their ordering is preserved. This raises the question of "ordered according to what metric", as concurrency is in play, so the nature of this property may vary by event.

This is only in the general case, as some events may not be connected to database transactions, some consumers might tolerate violations of either atomic success or failure, and not all events may have strict notions of ordering. However, in the general case violations of any of these can result in consistency failures between services that might not be corrected over any time scale.

It's also worth noting a goal we don't have, that of avoiding duplication. At-least-once delivery is acceptable; exactly-once delivery is not required. Double-sends of events are permissible as long as this only happens occasionally (for performance reasons) and does not entail a violation of ordering.

As of 2023-11-09 we produce events in two different ways relative to transactions:

- **Immediate send**: The event is produced to the event bus immediately upon the signal being sent, which will generally occur inside Django's request-level transaction (if using ``ATOMIC_REQUESTS``). This preserves atomicity in the success case as long as the broker is reachable, even if the IDA crashes -- but it does not preserve atomicity when the transaction fails. There is also no ordering guarantee in the case of concurrent requests.
- **On-commit send**: The event is only sent from a ``django.db.transaction.on_commit`` callback. This preserves atomicity in the failure case, but the IDA could crash after transaction commit but before calling the broker -- or more commonly, the broker could be down or unreachable, and all of the on-commit-produced events would be lost during that interval. Ordering is also not preserved here.

We currently use an ad-hoc mix of immediate and on-commit send in edx-platform, depending on how particular OpenEdxPublicSignals are emitted. For example, the code path for ``COURSE_CATALOG_INFO_CHANGED`` involves an explicit call to ``django.db.transaction.on_commit`` in order to ensure an on-commit send is used. But most signals do not have any such call, and are likely sent immediately. This uncontrolled state reflects our iterative approach to the event bus as well as our choice to start with events that are backed by other synchronization measures which can correct for consistency issues. However, we'd like to start handling events that require stronger reliability guarantees, such as those in the ecommerce space.

Decision
********

We will implement the transactional outbox pattern (or just "outbox pattern") in order to allow binding event production to database transactions. Events will default to on-commit send, but openedx-events configuration will be enhanced to allow configuring each event to a choice of production mode (on-commit or outbox).

In the outbox pattern, events are not produced as part of the request/response cycle, but are instead appended to an "outbox" database table within the transaction. A worker process operating in a separate transaction works through the list in order, producing them to the message broker and removing them once the broker has acknowledged them. This is the standard solution to the dual-write problem and is likely the only way to meet all of the criteria. Atomicity is ensured by bringing the *intent* to send an event into the transaction's ACID guarantees. Transaction commits also impose a meaningful ordering across all hosts using the same database.

openedx-events will change to support two producer modes for sending events when ``send(...)`` is called:

- ``on-commit``: Delay sending to the event bus until after the current transaction commits, or immediately if there is no open transaction (as might occur in a worker process).

  This requires ensuring that any events that are currently being explicitly sent on-commit are changed to call ``get_producer().send(...)`` directly, after appropriate per-event configuration. ``emit_catalog_info_changed_signal`` is a known example of this.
- ``outbox``: Prep the signal for sending, and save in an outbox table for sending as soon as possible. The outbox table will be managed by `django-jaiminho`_. Deployers using this mode will also need to run a jaiminho management command in a perpetual worker process in order to relay events from the outbox to the broker and mark them as successfully sent. Another management command would be needed to periodically purge old processed events.

  (TBD: Format for the event data in the outbox. No further event-specific DB queries should be required for producing the bytes for the wire format, but it should not be serialized in a way that is specific to Kafka, Redis, etc.)

  (TBD: Safeguards around inadvertently changing the save-to-outbox function's name and module, since those are included in jaiminho's outbox records.)

openedx-events will add a per event type configuration field specifying the event’s producer mode in the form of a new key-topic field inside ``EVENT_BUS_PRODUCER_CONFIG``. It will also add a new Django setting ``EVENT_BUS_PRODUCER_MODE`` that names a mode to use when not otherwise specified (defaulting to ``on-commit``.)

This will remove the ability to send an event immediately, as none of the currently implemented events would benefit from it. If in the future there is an event type that requires it, perhaps because it represents a request or attempt or even a failure, an ``immediate`` mode can be added.

``django-jaiminho`` will be added as a dependency of openedx-events and to the ``INSTALLED_APPS`` of relying IDAs.

TBD: Observability of outbox size and event send errors.

.. _django-jaiminho: https://github.com/loadsmart/django-jaiminho

Consequences
************

- The event bus becomes far more reliable, and able to handle events that require at-least-once delivery. The need for manual re-producing of events should become very rare.
- The new outbox functionality, if used, comes with operational complexity. Adding a new worker process to every service that produces events will further increase the orchestration needs of Open edX. (See alternatives section for a possible workaround.)
- Duplication becomes possible, so we would need a way to avoid sending the same event over and over again to the broker if the broker is failing to send acknowledgments. We may need to revisit existing events and improve documentation around ensuring that consumers can tolerate duplication, either by ensuring that events are idempotent or by keeping track of which event IDs have already been processed.
- The database will be required to store an unbounded number of events during a broker outage, worker outage, or event bus misconfiguration.

Rejected and Unplanned Alternatives
***********************************

Change Data Capture
===================

Change data capture (CDC) is a method of directly streaming database changes from one place to another by following the DB's transaction log. This provides the same transactionality benefits as the outbox method. `Debezium <https://debezium.io/>`_ is an example of such a system and can read directly from the database and produce to Kafka, where the data can then be transformed and routed to other systems. While a CDC platform could send data to the Open edX event bus, it would also be redundant with the event bus. In the example of Debezium, a deployment would still need a Kafka cluster even if they wanted to put event data into Redis.

CDC systems also source their data at a lower level than we're targeting with the event bus; Django usually insulates us from schema details via an ORM layer, but CDC involves reading table data directly. We'd have tight coupling with our DB schemas. And the eventing system we've chosen to build operates at a higher abstraction layer than database writes, creating another conceptual mismatch. Theoretically, a CDC system could also be responsible for reading events from an outbox, allowing high-level eventing, but this is unlikely to be more palatable than just running a management command in a loop.

Non-worker event production
===========================

The outbox pattern usually involves running a worker process that handles moving data from the outbox to the broker. However, it may be possible for deployers to avoid this with the use of some alternative middleware. For example, a custom middleware could flush events to the broker at the end of each event-producing request. The middleware's ``post_response`` would run outside of the request's main transaction. It would check if the request had created events, and if so, it would pull *at least that many* events from the outbox and produce them to the broker, then remove them from the outbox. If the server crashed before this could complete, later requests would eventually complete the work. This would also cover events produced by workers and other non-request-based processes.

Web responses that produce events would have higher latency, as they would have to finish an additional DB read, broker call, and DB write before returning the response to the user. Event latency would also increase and become more variable due to the opportunistic approach.

It's also conceivable that each Django server in the IDA could start a background process to act as an outbox-emptying worker.

We're not planning on implementing either of these, but they should be drop-in replacements for the long-running management command, and could be developed in the future by deployers who need such an arrangement.

References
**********

- Microservices.io on the transactional outbox pattern: https://microservices.io/patterns/data/transactional-outbox.html
- An introduction to jaiminho: https://engineering.loadsmart.com/blog/introducing-jaiminho

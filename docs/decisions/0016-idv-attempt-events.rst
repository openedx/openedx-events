16. Event definitions for ID Verification
#########################################

NOTE: This decision doc is still a work in progress.

Status
******

**Draft** 2024-08-19

Context
*******

IDV Change:
===========
* We're changing it b/c software secure no longer supports IDV

The IDV Vendor:
===============
* Persona


Decision
********

Where these events will be produced/consumed:
=============================================

<!-- This is based off the special exam decision doc, lmk if this is wrong -->
* `persona-integration` will produce these events.
* NOTE: There is no plan to have the legacy backend in `edx-platform`, produce these events.
* `edx-platform` will consume these events in order to handle all behavior as it pertains to the state of an ID Verification.

Event Definitions:
==================
<!-- NOTE: do we have to do this? -->
* We will define the events that as planned in `the ADR for events in persona_integration <insert url here>`_.

Consequences
************

* The `verify_student` app will emit events via the event bus to send information without needing a response.
* These events are dynamic, in that they can also be consumed by other services/applications as needed in the future.


16. Event definitions for ID Verification
#########################################

Status
******

**Draft** 2024-08-28

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
* The intention is for the verify_student application to produce these events.
* These events should be vendor agnostic and should not produced by any IDV plugin.
* `edx-platform` will consume these events in order to handle all behavior as it pertains to the state of an ID Verification.

Event Definitions:
==================
* We will define the events that as planned in `the ADR for events in persona_integration <https://2u-internal.atlassian.net/wiki/spaces/COSMO/pages/1183645808/Diff+Spec+Persona+Integration#%5BhardBreak%5DEvent-Hooks>`_.

Consequences
************

* The `verify_student` app will emit events to send information to other applications, which can be handled as normal Django signals.
* These events are dynamic, in that they can also be consumed by other services/applications as needed in the future.

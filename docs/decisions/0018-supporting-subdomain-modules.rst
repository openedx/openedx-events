.. _ADR-18:

0018: Supporting Subdomain Modules for Cross-Domain Events
##########################################################

Status
******

**Proposed**

Context
*******

Events in ``openedx-events`` are organized into domain modules (e.g., ``learning``,
``course_authoring``) following the Open edX architecture subdomains in
:ref:`Architecture Subdomains Reference`. This works well when an event belongs
to a single subdomain.

The `edX DDD Bounded Contexts`_ documentation classifies subdomains as core,
supporting, or generic. Supporting subdomains provide capabilities that multiple
core subdomains depend on, without belonging to any of them. ``analytics`` is the
existing example in ``openedx-events``.

Authorization has the same character: role assignment events originate from
``openedx-authz`` and could be consumed across learning, content authoring, enterprise,
and other areas. Its domain definition is independent of any single application,
so the ``authz`` module introduced in this ADR is classified as supporting.

Prior to this decision, there was no explicit guidance for supporting subdomain
events, leaving contributors to make ad-hoc placement choices.

Decision
********

We introduce dedicated top-level modules in ``openedx-events`` for supporting
subdomains when their events cannot be meaningfully attributed to a single
existing domain module.

A supporting subdomain module is warranted when:

* The subdomain provides a capability that multiple core subdomains depend on.
* The events are meaningful to consumers across existing domain modules without
  a clear primary owner among them.
* Placing the events in any single existing domain module would reflect a
  current implementation detail rather than a stable domain boundary.

The ``authz`` module introduced in this branch applies this pattern to
authorization events. The existing ``analytics`` module is recognized as a prior
instance of the same concept.

Consequences
************

1. Supporting subdomain events have a principled home grounded in the Open edX
   DDD taxonomy, rather than an arbitrary placement.
2. The pattern is consistent with how ``analytics`` is already organized, and
   both are now explicitly grounded in the same classification.
3. Supporting subdomain modules can evolve independently of any single
   application's release cycle.
4. Deciding whether a concern qualifies as a supporting subdomain requires
   judgment. Without discipline, this can lead to module proliferation.

Rejected Alternatives
*********************

* **Place authorization events under ``course_authoring``**: role assignment is
  currently performed through an admin console accessed via Studio, but that is
  a transitional implementation detail. The admin console is planned to evolve
  into its own application, and role assignment is semantically an authorization
  concern, not a content authoring one.
* **Create a generic ``admin`` module**: authorization has a self-contained domain
  definition that stands independently of any UI surface. "Admin" describes a user
  role and an interface where tasks from multiple domains are aggregated - the
  tasks themselves belong to their respective domains.
* **Extend an existing module with a subdirectory**: this would misrepresent the
  domain ownership of the events and contradict the existing top-level module
  structure.

References
**********

- `edX DDD Bounded Contexts`_
- :ref:`Architecture Subdomains Reference`

.. _edX DDD Bounded Contexts: https://openedx.atlassian.net/wiki/spaces/AC/pages/663224968/edX+DDD+Bounded+Contexts

2. Open edX events naming
=========================

Status
------

Draft

Context
-------

Besides a suitable location, event-type hooks need a form of
identification when adding them to the Open edX platform. By doing this,
recognizing which event to use, or debugging errors will be easier.

This ADR has the purpose of defining the rules to be followed when
naming an Open edX Event.

Decisions
---------

1. Given that signals don't have an explicit name, the identifier will be
the module path and variable where the signal is stored.

2. While trying to follow the format defined in the `OEP-41`_:

``{Reverse DNS}.{Architecture Subdomain}.{Subject}.{Action}.{Major Version}``

We encountered two major issues for our use case:

* Reverse DNS: if we use the namespace ``org.openedx``, then our package would
  be ``openedx-events/org/openedx/openedx_events/.../`` which will break
  conventions for Python packages in the Open edX ecosystem. To be consistent,
  the proposal is to remove ``Reverse DNS`` and use a ``Namespace`` that in our
  case would be ``openedx_events``.

* Major version location: following the same idea, when using ``Major version``
  at the end, the name would be ``/openedx_events/.../action/`` meaning the
  signal will be stored in the variable v1, which is not suitable given our
  architecture. To be consistent with our design, the proposal is to place
  ``Major Version`` before ``Subject``.

Applying the proposals will result in:

``{Namespace}.{Architecture Subdomain}.{Major Version}.{Subject}.{Action}``

Examples:

* openedx_filters.learning.v1.course.enrollment.created
* openedx_filters.learning.v1.student.registration.completed
* openedx_filters.learning.v1.session.login.completed

.. _OEP-41: https://open-edx-proposals.readthedocs.io/en/latest/oep-0041-arch-async-server-event-messaging.html#specification

Consequences
------------

* All events defined in this repository must follow the same format.

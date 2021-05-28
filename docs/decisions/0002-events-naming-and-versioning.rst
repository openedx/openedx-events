2. Open edX events naming and versioning
========================================

Status
------

Accepted


Context
-------

Event type hooks are an important public promise. They are a strong foundation
of a healthy ecosystem of extensions for the Open edX world and have been
recognized as such by the arch team of the Open edX core and also by the community.

This ADR has the purpose of defining the rules to be followed when naming an
Open edX Event with the intent of covering the use cases of:

* Open edX core developers wanting to add new events.
* Open edX core developers wanting to deprecate and eventually remove events.
* Open edX extension developers wanting to create and maintain stable
  applications, even when the events framework evolves and changes over time.
* Service developers wanting to listen for events using message queues.

The decisions reached in this ADR are the product of open discussions in the ADR
PR history.


Decisions
---------

1. The name of an event will be a ``string`` that follows the `type format`_
defined in the `OEP-41`_:

``{Reverse DNS}.{Architecture Subdomain}.{Subject}.{Action}.{Major Version}``

Examples:

* org.openedx.learning.course.enrollment.created.v1
* org.openedx.learning.student.registration.completed.v2
* org.openedx.learning.session.login.completed.v1
* org.openedx.learning.session.login.completed.v1

2. The signal definitions will be placed written in code in the way that is more
practical and familiar for python developer with emphasis on Django experience.
Definition will be grouped by subdomain along with other data structures in a
way that favors reuse.
There will be a subclass of Django signal that accepts the event name and makes
available for listeners of the emitted events and the frameworks other event
processing queues. Only the Architecture Subdomain part of the event name will
be used in the package name of the signal definition.

3. The events library will use SemVer 2. The major version will not be tied to
Open edX releases for the time being. We still recognize that Open edX releases
are the logical boundary to remove signals and therefore make breaking changes
such as remove signal definitions.

4. The Major version of an event will be both part of the `event name` and also
be written to the variable defining the signal. However version 1 (V1) of an
event will remove the _V1 suffix for readability. We also expect to have
relatively few breaking changes to the signal definitions. The minor version of
a signal will be written in the payload as part of the header information
defined in `OEP-41`_.

5. The events library will be a single library containing the signal definitions,
the simple data structures required and the necessary classes and tools to
support the events framework. The definitions of the signals will be written
with a logical boundary such that if the project ever decides to separate them
in a split library there is no necessary large refactor.

.. _type format: https://open-edx-proposals.readthedocs.io/en/latest/oep-0041-arch-async-server-event-messaging.html#id5
.. _OEP-41: https://open-edx-proposals.readthedocs.io/en/latest/oep-0041-arch-async-server-event-messaging.html#specification


Consequences
------------

1. There will not be a necessary correspondence between open edX release and
major versions of this library. Also there will not be a need to make a major
release if there is no breaking for consecutive Open edX releases.

2. Open edX core and in particular edx-platform must emit the signals meant for
public consumption as they are written in this library, changes in edx-platform
that require changes in the public signal will require a backwards compatible
addition to this library or an altogether new signal with support for the old
signal until deprecated and removed.

3. Changing the arguments passed to an event must always be done in a backwards
compatible way since making it incompatible warrants the use of a new major
version.

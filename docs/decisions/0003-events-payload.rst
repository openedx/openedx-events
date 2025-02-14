3. Open edX events payload conventions
======================================

Status
------

**Accepted**


Context
-------

Given their public promise status, event hooks have maintainability as the main
design goal. The contracts we are creating here should be stable enough to
support the growth of the extensions community. That said, things should be
allowed to evolve in a backwards compatible manner. When things inevitable break,
they should break in CI. Which should not require the code of the Open edX platform to
test integrations.


Decisions
---------

1. Events will receive header information in line with the `OEP-41 format`_.
However all the fields but `data`, which are also referred as the envelope
information, will be wrapped in a dictionary. The data specific to the event
will be passed as unpacked named arguments so that function signature mismatch
errors can be caught in CI.

2. The envelope information will be calculated on the fly by the
`OpenEdxPublicSignal` class to keep this information out of the way when writing
the event calling location as well.

3. The data sent to an event will always use the form of attr objects following
the `OEP-49 data pattern`_ . This data objects will be defined in the events
library and will be scoped to the Architecture Subdomain they are in. Data
objects should use only serializable python primitives and standard types with
the exception of OpaqueKeys.


.. _OEP-41 format: https://open-edx-proposals.readthedocs.io/en/latest/oep-0041-arch-async-server-event-messaging.html#message-format
.. _OEP-49 data pattern: https://open-edx-proposals.readthedocs.io/en/latest/oep-0049-django-app-patterns.html#id9


Consequences
------------

1. Extension developers will be able to test their event listeners without the
need to import any Open edX platform code.

2. Consequence of the versioning ADR together with this one, extension developers
will be able to test their code with different versions of the library and thus
guarantee that their code will not break when upgrading open releases.

3. The events library will have a dependency on the OpaqueKeys library.

4. Events defined by this library will not be drop-in replacement of current
Open edX platform signals. This means some refactoring will be needed when converting
the platform code over to openedx_events.

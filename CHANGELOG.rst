Change Log
==========

..
   All enhancements and patches to openedx_events will be documented
   in this file.  It adheres to the structure of https://keepachangelog.com/ ,
   but in reStructuredText instead of Markdown (for ease of incorporation into
   Sphinx documentation and the PyPI description).

   This project adheres to Semantic Versioning (https://semver.org/).

.. There should always be an "Unreleased" section for changes pending release.

Unreleased
----------

[9.8.0] - 2024-04-11

Added
~~~~~
* Added support for Python 3.11

[9.7.0] - 2024-04-04
--------------------
Added
~~~~~~~
* Added new ``SUBSIDY_REDEEMED`` and ``SUBSIDY_REDEMPTION_REVERSED`` events in enterprise.

[9.6.0] - 2024-04-01
--------------------
Added
~~~~~~~
* Added new ``CONTENT_OBJECT_TAGGED`` events in content_authoring.

[9.5.2] - 2024-02-13
--------------------
Removed
~~~~~~~
* Remove unused ``MANAGE_STUDENTS_PERMISSION_ADDED`` and ``MANAGE_STUDENTS_PERMISSION_REMOVED`` events in learning

[9.5.1] - 2024-02-12
--------------------
Changed
~~~~~~~
* Fixed recursion error when consuming events on the same service that produced them.

[9.5.0] - 2024-02-07
--------------------
Added
~~~~~
* Adds utility function to reset application state similar to setup/teardown in Django request/response cycle.

[9.4.0] - 2024-01-29
--------------------
Added
~~~~~
* Added new ``COURSE_ACCESS_ROLE_ADDED`` and ``COURSE_ACCESS_ROLE_REMOVED`` events in learning

[9.3.0] - 2024-01-24
--------------------
Changed
~~~~~~~
* Allow new EVENTS_SERVICE_NAME setting to override SERVICE_VARIANT for data source.

[9.2.0] - 2023-11-16
--------------------
Added
~~~~~~~
* Added new COURSE_NOTIFICATION_REQUESTED event in learning

[9.1.0] - 2023-11-07
--------------------
Added
~~~~~~~
* Added new event TRACKING_EVENT_EMITTED.

[9.0.1] - 2023-10-31
--------------------
Changed
~~~~~~~
* Fixed key error in merging event producer configs. Previously, setting only one of `enabled` or `event_key_field` would result in a KeyError being thrown

[9.0.0] - 2023-10-04
--------------------
Changed
~~~~~~~
* Re-licensed this repository from AGPL 3.0 to Apache 2.0
* **Breaking change**: Restructured EVENT_BUS_PRODUCER_CONFIG

[8.9.0] - 2023-10-04
--------------------
Added
~~~~~
* Added new ``FORUM_THREAD_CREATED``, ``FORUM_THREAD_RESPONSE_CREATED``, ``FORUM_RESPONSE_COMMENT_CREATED`` events in learning subdomain

[8.8.0] - 2023-10-02
--------------------
Added
~~~~~
* Added new ``MANAGE_STUDENTS_PERMISSION_ADDED`` and ``MANAGE_STUDENTS_PERMISSION_REMOVED`` events in learning

[8.7.0] - 2023-09-29
--------------------
Added
~~~~~
* Added new ``EXAM_ATTEMPT_SUBMITTED``, ``EXAM_ATTEMPT_REJECTED``, ``EXAM_ATTEMPT_VERIFIED``, ``EXAM_ATTEMPT_RESET``, and ``EXAM_ATTEMPT_ERRORED`` events in learning.

[8.6.0] - 2023-08-28
--------------------
Added
~~~~~
* Added generic handler to allow producing to event bus via django settings.

[8.5.0] - 2023-08-08
--------------------
Changed
~~~~~~~
* Added json de/serialization for EventsMetadata

[8.4.0] - 2023-07-20
--------------------
Added
~~~~~
* Added new ``PROGRAM_CERTIFICATE_AWARDED`` and ``PROGRAM_CERTIFICATE_REVOKED`` events in learning subdomain
* Added new ``ProgramCertificateData`` and ``ProgramData`` data classes supporting the new program certificate events

[8.3.0] - 2023-07-10
--------------------
Added
~~~~~
* Added new XBLOCK_CREATED and XBLOCK_UPDATED events in content_authoring.
* Added new COURSE_CREATED event in content_authoring.
* Added new CONTENT_LIBRARY_CREATED, CONTENT_LIBRARY_UPDATED and CONTENT_LIBRARY_DELETED events in content_authoring.
* Added new LIBRARY_BLOCK_CREATED, LIBRARY_BLOCK_UPDATED and LIBRARY_BLOCK_DELETED events in content_authoring.

[8.2.0] - 2023-06-08
--------------------
Changed
~~~~~~~
* Added new USER_NOTIFICATION_REQUESTED event.

[8.1.0] - 2023-06-06
--------------------
Added
~~~~~
* Store current versions of Avro schemas and add test to ensure valid evolution

[8.0.1] - 2023-05-16
--------------------
Changed
~~~~~~~
* Fixed event_type of XBLOCK_SKILL_VERIFIED signal

[8.0.0] - 2023-05-16
--------------------
Changed
~~~~~~~
* **Breaking change**: Remove ``signal`` argument from consume_events and make_single_consumer

[7.3.0] - 2023-05-15
--------------------
Changed
~~~~~~~
* Made `signal` argument optional in consume_events in preparation for removal

[7.2.0] - 2023-05-03
--------------------
Changed
~~~~~~~
* Added event type as namespace to generated Avro schemas


[7.1.0] - 2023-05-03
--------------------
Added
~~~~~
* Configurable loader for consumer side of Event Bus in ``openedx_events.event_bus``.
* Added management command to load configured consumer and start worker.

Changed
~~~~~~~
* Switch from ``edx-sphinx-theme`` to ``sphinx-book-theme`` since the former is
  deprecated.  See https://github.com/openedx/edx-sphinx-theme/issues/184 for
  more details.

[7.0.0] - 2023-03-07
---------------------
Changed
~~~~~~~
* **Breaking change**: Moved serialize_event_data_to_bytes from openedx_events.event_bus.avro.tests.test_utilities to openedx_events.event_bus.avro.serializer
* **Breaking change**: Moved deserialize_bytes_to_event_data from openedx_events.event_bus.avro.tests.test_utilities to openedx_events.event_bus.avro.deserializer

[6.0.0] - 2023-02-23
---------------------
Changed
~~~~~~~
* **Breaking change**: Moved load_all_events() from openedx_events.tests.utils to openedx_events.tooling

[5.1.0] - 2023-02-07
---------------------
Added
~~~~~~~
* Added support for array type.
* Added new XBLOCK_SKILL_VERIFIED event.
* Added XBlockSkillVerificationData classes.

[5.0.0] - 2023-02-03
--------------------
Changed
~~~~~~~
* **Breaking change**: ``send_event_with_custom_metadata`` changes to accept a single EventsMetadata object rather than all of the fields that go into one. This only directly affects event bus consumer libraries.

Added
~~~~~
* Added ``COURSE_CERTIFICATE_CONFIG_CHANGED`` and ``COURSE_CERTIFICATE_CONFIG_DELETED`` signals for when a course's certificate configuration is updated or deleted

[4.2.0] - 2023-01-24
--------------------
Added
~~~~~
* Added ``send_event_with_custom_metadata``. This will enable event bus consumers to send the event signal with the same metadata fields that were used when the event was produced.

Fixed
~~~~~
* Updated time metadata to include UTC timezone. The original implementation used utcnow(), which could give different results if the time were ever interpreted to be local time. See https://docs.python.org/3/library/datetime.html#datetime.datetime.utcnow
* EventsMetadata minorversion is now fully optional, and doesn't need to be supplied when initializing to get the default of 0.

Changed
~~~~~~~
* Updated send_event with an optional time argument to be used as metadata.

[4.1.1] - 2023-01-23
---------------------
Changed
~~~~~~~
* Use collections.abc import to use with python 3.8 and 3.10.

[4.1.0] - 2023-01-03
---------------------
Added
~~~~~
* Added new XBLOCK_PUBLISHED, XBLOCK_DUPLICATED and XBLOCK_DELETED signals in content_authoring.
* Added XBlockData and DuplicatedXBlockData classes
* Added custom UsageKeyAvroSerializer for opaque_keys UsageKey.

[4.0.0] - 2022-12-01
--------------------
Changed
~~~~~~~
* **Breaking change** Make event_metadata parameter in EventBusProducer send API required

[3.2.0] - 2022-11-30
--------------------
Changed
~~~~~~~
* Add event_metadata parameter to EventBusProducer send API.  **Note:** Calling this method with the new argument will throw an exception with older versions of this library that don't yet support the parameter.

[3.1.0] - 2022-11-22
--------------------
Added
~~~~~
* Configurable loader for producer side of Event Bus in ``openedx_events.event_bus``.

[3.0.1] - 2022-10-31
--------------------
Fixed
~~~~~
* Fix default value for optional fields from "null" to None

[3.0.0] - 2022-10-19
--------------------
* **Breaking change**: Removed (optional) field ``effort`` from ``CourseCatalogData.`` Nothing should be relying on this field as it is not used by Course Discovery in Publisher-enabled setups.

[2.0.0] - 2022-10-18
--------------------
* **Breaking change**: Removed signal ``SUBSCRIPTION_LICENSE_MODIFIED`` and corresponding data class ``SubscriptionLicenseData``. This should only affect experimental event-bus code (which should also have been deleted by now).

[1.0.0] - 2022-09-27
--------------------
* **Breaking Change**: Updated from ``Django 2.0`` to ``Django 3.0``.
* Bump version to 1.x to acknowledge that this is in use in production

[0.14.0] - 2022-09-21
---------------------
Changed
~~~~~~~
* **Breaking change**: Removed ``short_description`` from ``CourseCatalogData``

[0.13.0] - 2022-09-16
---------------------
Added
~~~~~
* Added new event PERSISTENT_GRADE_SUMMARY_CHANGED.

* Improvements in make upgrade command and requirements files.
* Manually update requirements files to fix requirements bot issue with pip/setup tools.
* Change GitHub workflow to community maintained repository health file.

[0.12.0] - 2022-08-16
---------------------
Changed
~~~~~~~
* **Breaking change**: Removed ``org`` and ``number`` fields from ``CourseCatalogData``
  (should only affect unreleased event-bus code, though)

[0.11.1] - 2022-07-28
---------------------
Fixed
~~~~~
* Handle optional (None) values for custom serializers

[0.11.0] - 2022-07-21
---------------------
Added
~~~~~
* Added new content_authoring module with new COURSE_CATALOG_INFO_CHANGED signal

[0.10.0] - 2022-05-20
---------------------
Changed
~~~~~~~
* BREAKING CHANGE: Split AvroAttrsBridge into schema, serialization, and deserialization phases

[0.9.1] - 2022-05-20
--------------------
Changed
~~~~~~~
* Remove assigned_email from SubscriptionLicenseData

[0.9.0] - 2022-04-28
--------------------
Changed
~~~~~~~
* Updated AvroAttrsBridge to handle optional/nullable fields

[0.8.3] - 2022-04-26
--------------------
Changed
~~~~~~~
* Updated AvroAttrsBridge to create schemas from signal data dict rather than individual attrs classes

[0.8.2] - 2022-04-13
--------------------
Changed
~~~~~~~
* Changed openedx_events.learning.data.DiscussionTopicContext to make the group id optional
* Changed DiscussionTopicContext to add a `context` attribute

[0.8.1] - 2022-03-03
--------------------

Added
~~~~~
* Added missing field for event COURSE_DISCUSSIONS_CHANGED

[0.8.0] - 2022-02-25
--------------------
Added
~~~~~
* Added COURSE_DISCUSSIONS_CHANGED for discussion event

Changed
~~~~~~~
* Changed openedx_events/enterprise/LicenseLifecycle class to openedx_events/enterprise/SubscriptionLicenseData
* Changed LicenseCreated signal class to SUBSCRIPTION_LICENSE_MODIFIED signal class

[0.7.1] - 2022-01-13
--------------------
Added
~~~~~
* Added data definition for enterprise/LicenseLifecycle
* Added LicenseCreated signal definition

[0.7.0] - 2022-01-06
--------------------
Added
~~~~~
* Added AvroAttrsBridge class to convert between avro standard and attrs classes

[0.6.0] - 2021-09-15
--------------------
Added
~~~~~
* Add custom formatting class for events responses.
* Add a way to use send method instead of send_robust while testing.

Changed
~~~~~~~
* Remove unnecessary InstantiationError exception.
* Default is send_robust instead of send unless specified otherwise.

[0.5.1] - 2021-08-26
--------------------
Changed
~~~~~~~
* Remove TestCase inheritance from OpenEdxTestMixin.

[0.5.0] - 2021-08-24
--------------------
Added
~~~~~
* Utilities to use while testing in other platforms.

[0.4.1] - 2021-08-18
--------------------
Changed
~~~~~~~
* Remove raise_exception assignment in events metadata.

[0.4.0] - 2021-08-18
--------------------
Added
~~~~~
* Preliminary Open edX events definitions.

[0.3.0] - 2021-08-18
--------------------
Added
~~~~~
* Add tooling needed to create and trigger events in Open edX platform.
* Add Data Attribute classes used as arguments by Open edX Events.


[0.2.0] - 2021-07-28
--------------------
Changed
~~~~~~~

* Update repository purpose.
* Changed max-doc-length from 79 to 120 following community recommendation.

[0.1.3] - 2021-07-01
--------------------
Changed
~~~~~~~

* Update setup.cfg with complete bumpversion configuration.

[0.1.2] - 2021-06-29
--------------------
Changed
~~~~~~~

* Update documentation with current organization info.

[0.1.1] - 2021-06-29
--------------------
Added
~~~~~

* Add Django testing configuration.

[0.1.0] - 2021-04-07
--------------------

Added
~~~~~

* First release on PyPI.

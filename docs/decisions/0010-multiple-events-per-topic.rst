9. Combining multiple event types on one topic
==============================================

Status
------

Accepted

Context
-------
As initially implemented, the Kafka-backed event bus assumed that every topic would only have events of one type.

Decision
--------

The COURSE_CATALOG_INFO_CHANGED will only contain the information necessary to work in a Publisher-enabled environment. In particular, this means it will not include some fields usually present in the Studio ``/courses`` API endpoint, for example:
- ``media``
- ``short_description``
- ``mobile_available``
- ``effort``

In Discovery, if Publisher is not enabled, the consumer will log a warning and not try to update anything.

Rationale
---------

The way we update media information in refresh-course-metadata is quite haphazard, with no real standard way of sending over the information or of storing it on the Discovery end. Replicating these structures in the COURSE_CATALOG_INFO_CHANGED signal would make the data definition confusing. In addition, it is very difficult to test these other fields without a real non-Publisher environment that runs refresh-course-metadata.

Until these fields are needed by a consumer in a non-Publisher environment (if ever), it makes sense to defer trying to find a good solution to this problem.

Deferred work
-------------
It is possible in the future we will want to use this event to sync data between Studio and Discovery in systems that do not include Publisher. At that time, we can work on cleaning up the media data structures for cleaner event definitions.

Github discussion
-----------------
For discussion on the initial event design, see https://github.com/openedx/openedx-events/issues/72 .
For discussion on the removal of the media fields, see the comments on this PR: https://github.com/openedx/openedx-events/pull/81 .

Change history
--------------

2022-10-18
~~~~~~~~~~
- Updated `Decision` section to include more excluded fields

2022-09-14
~~~~~~~~~~
Initial commit

8. Event design of the COURSE_CATALOG_INFO_CHANGED signal
=========================================================

Status
------

Provisional

Context
-------

The COURSE_CATALOG_INFO_CHANGED signal is used by Studio to convey that information relevant to the course catalog has changed. It was created with an eye towards eventually replacing the refresh-course-metadata batch job, which syncs all data between edx-platform and course-discovery.

Refresh-course-metadata functions differently depending on whether or not the system has Publisher enabled. Specifically, after requesting information from the ``/courses`` endpoint in Studio, Discovery will ignore certain fields if Publisher is enabled. These fields are mostly part of the ``media`` attribute of the API response. They are sent in a variety of ways (absolute urls, paths, sometimes divided by size, etc.)

Decision
--------

The COURSE_CATALOG_INFO_CHANGED will only contain the information necessary to work in a Publisher-enabled environment. In particular, this means it will not contain the ``media`` field usually present in the Studio ``/courses`` API endpoint.

In Discovery, if Publisher is not enabled, the consumer will log a warning and not try to update anything.

Rationale
---------

The way we update media information in refresh-course-metadata is quite haphazard, with no real standard way of sending over the information or of storing it on the Discovery end. Replicating these structures in the COURSE_CATALOG_INFO_CHANGED signal would make the data definition confusing. Moreover, edx.org has Publisher enabled and would thus ignore these fields anyway.

Deferred work
-------------
It is possible in the future we will want to use this event to sync data between Studio and Discovery in systems that do not include Publisher. At that time, we can work on cleaning up the media data structures for cleaner event definitions.

Github discussion
-----------------
For discussion on the initial event design, see https://github.com/openedx/openedx-events/issues/72 .
For discussion on the removal of the media fields, see the comments on this PR: https://github.com/openedx/openedx-events/pull/81 .


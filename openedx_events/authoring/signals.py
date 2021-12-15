"""
Custom signals definitions that representing the Open edX platform events.

All signals defined in this module must follow the name and versioning
conventions specified in docs/decisions/0002-events-naming-and-versioning.rst

They also must comply with the payload definition specified in
docs/decisions/0003-events-payload.rst
"""
from openedx_events.authoring.data import CourseBlockData
from openedx_events.tooling import OpenEdxPublicSignal


# .. event_type: org.openedx.authoring.course.created.v1
# .. event_name: COURSE_CREATED
# .. event_description: emitted when the course creation registration process through Studio is completed.
# .. event_data: CourseBlockData
COURSE_CREATED = OpenEdxPublicSignal(
    event_type="org.openedx.authoring.course.created.v1",
    data={
        "course": CourseBlockData,
    }
)


# .. event_type: org.openedx.authoring.course_start.changed.v1
# .. event_name: COURSE_START_DATE_CHANGED
# .. event_description: emitted when the course creation registration process through Studio is completed.
# .. event_data: CourseBlockData
COURSE_START_DATE_CHANGED = OpenEdxPublicSignal(
    event_type="org.openedx.authoring.course_start.changed.v1",
    data={
        "course": CourseBlockData,
    }
)


# .. event_type: org.openedx.authoring.course_pacing.changed.v1
# .. event_name: COURSE_START_DATE_CHANGED
# .. event_description: emitted when the course creation registration process through Studio is completed.
# .. event_data: CourseBlockData
COURSE_PACING_CHANGED = OpenEdxPublicSignal(
    event_type="org.openedx.authoring.course_pacing.changed.v1",
    data={
        "course": CourseBlockData,
    }
)


# .. event_type: org.openedx.authoring.course.details.changed.v1
# .. event_name: COURSE_ADVANCED_SETTINGS_CHANGED
# .. event_description: emitted when the course creation registration process through Studio is completed.
# .. event_data: CourseBlockData
COURSE_ADVANCED_SETTINGS_CHANGED = OpenEdxPublicSignal(
    event_type="org.openedx.authoring.course_advanced_settings.changed.v1",
    data={
        "course": CourseBlockData,
    }
)

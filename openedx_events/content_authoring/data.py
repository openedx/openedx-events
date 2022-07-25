"""
Data attributes for events within the architecture subdomain ``content_authoring``.

These attributes follow the form of attr objects specified in OEP-49 data
pattern.

The attributes for the events come from the CourseDetailView in the LMS, with some unused fields removed
(see deprecation proposal at https://github.com/openedx/public-engineering/issues/160)
"""
from datetime import datetime

import attr
from opaque_keys.edx.keys import CourseKey


@attr.s(frozen=True)
class CourseScheduleData:
    """
    Data describing course scheduling.

    Arguments:
        start (datetime): course start date
        pacing (str): 'instructor' or 'self'
        end (datetime): course end date (optional)
        enrollment_start (datetime): start of course enrollment (optional)
        enrollment_end (datetime): end of course enrollment (optional)
    """

    start = attr.ib(type=datetime)
    pacing = attr.ib(type=str)
    end = attr.ib(type=datetime, default=None)
    enrollment_start = attr.ib(type=datetime, default=None)
    enrollment_end = attr.ib(type=datetime, default=None)


@attr.s(frozen=True)
class CourseCatalogData:
    """
    Data needed for a course catalog entry.

    Arguments:
        course_key (CourseKey): identifier of the Course object.
        name (str): course name
        org (str): course organization identifier
        number (str): course number
        schedule_data (CourseScheduleData): scheduling information for the course
        short_description (str): one- or two-sentence course description (optional)
        effort (str): estimated level of effort in hours per week (optional). Kept as a str to align with the lms model.
        hidden (bool): whether the course is hidden from search (optional)
        invitation_only (bool): whether the course requires an invitation to enroll
    """

    # basic identifiers
    course_key = attr.ib(type=CourseKey)
    name = attr.ib(type=str)
    number = attr.ib(type=str)
    org = attr.ib(type=str)

    # additional marketing information
    schedule_data = attr.ib(type=CourseScheduleData)
    short_description = attr.ib(type=str, default=None)
    effort = attr.ib(type=str, default=None)
    hidden = attr.ib(type=bool, default=False)
    invitation_only = attr.ib(type=bool, default=False)

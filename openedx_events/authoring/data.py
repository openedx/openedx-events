"""
Data attributes for events within the architecture subdomain `authoring`.

These attributes follow the form of attr objects specified in OEP-49 data
pattern.
"""
from datetime import datetime

import attr
from opaque_keys.edx.keys import CourseKey


@attr.s(frozen=True)
class UserData:
    """
    Attributes defined for Open edX user object.

    This class extends UserNonPersonalData to include PII data completing the
    user object.

    Arguments:
        id (int): unique identifier for the Django User object.
    """

    id = attr.ib(type=int)

@attr.s(frozen=True)
class CourseBlockData:
    """
    Attributes defined for Open edX Course Block object.

    Arguments:
        course_key (str): identifier of the Course object.
        display_name (str): display name associated with the course.
        start (datetime): start date for the course.
        end (datetime): end date for the course.
    """

    course_key = attr.ib(type=CourseKey)
    display_name = attr.ib(type=str)
    start = attr.ib(type=datetime)
    end = attr.ib(type=datetime)
    enrollment_start = attr.ib(type=datetime)
    enrollment_end = attr.ib(type=datetime)
    certificate_available_date = attr.ib(type=datetime)
    pacing = attr.ib(type=str)
    created_by = attr.ib(type=UserData, default=None)

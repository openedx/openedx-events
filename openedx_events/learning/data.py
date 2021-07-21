"""
Data attributes for events within the architecture subdomain `learning`.

These attributes follow the form of attr objects specified in OEP-49 data
pattern.
"""
from datetime import datetime
from typing import Dict

import attr
from opaque_keys.edx.keys import CourseKey


@attr.s(frozen=True)
class UserNonPersonalData:
    """
    Attributes defined for Open edX user object based on non-PII data.
    """

    id = attr.ib(type=int)
    is_active = attr.ib(type=bool, default=True)


@attr.s(frozen=True)
class UserPersonalData:
    """
    Attributes defined for Open edX user object based on PII data.
    """

    username = attr.ib(type=str)
    email = attr.ib(type=str)
    name = attr.ib(type=str, factory=str)


@attr.s(frozen=True)
class UserData:
    """
    Attributes defined for Open edX user object.
    """

    user_non_pii = attr.ib(type=UserNonPersonalData)
    user = attr.ib(type=UserPersonalData)


@attr.s(frozen=True)
class CourseData:
    """
    Attributes defined for Open edX Course Overview object.
    """

    course_key = attr.ib(type=CourseKey)
    display_name = attr.ib(type=str, factory=str)
    start = attr.ib(type=datetime, default=None)
    end = attr.ib(type=datetime, default=None)


@attr.s(frozen=True)
class CourseEnrollmentData:
    """
    Attributes defined for Open edX Course Enrollment object.
    """

    user = attr.ib(type=UserData)
    course = attr.ib(type=CourseData)
    mode = attr.ib(type=str)
    is_active = attr.ib(type=bool)
    creation_date = attr.ib(type=datetime)
    created_by = attr.ib(type=UserData, default=None)


@attr.s(frozen=True)
class CertificateData:
    """
    Attributes defined for Open edX Certificate data object.
    """

    user = attr.ib(type=UserData)
    course = attr.ib(type=CourseData)
    mode = attr.ib(type=str)
    grade = attr.ib(type=str)
    status = attr.ib(type=str)
    download_url = attr.ib(type=str)
    name = attr.ib(type=str)


@attr.s(frozen=True)
class CohortData:
    """
    Attributes defined for Open edX Cohort Membership object.
    """

    user = attr.ib(type=UserData)
    course = attr.ib(type=CourseData)
    name = attr.ib(type=str)

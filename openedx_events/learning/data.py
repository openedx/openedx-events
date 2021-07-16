"""
Data attributes for events within the architecture subdomain `learning`.

These attributes follow the form of attr objects specified in OEP-49 data
pattern.
"""
from datetime import datetime

import attr
from opaque_keys.edx.keys import CourseKey


@attr.s(frozen=True)
class UserNonPersonalData:
    """
    Attributes defined for Open edX user object based on non-PII data.

    Arguments:
        id (int): unique identifier for the Django User object.
        is_active (bool): indicates whether the user is active.
    """

    id = attr.ib(type=int)
    is_active = attr.ib(type=bool, default=True)


@attr.s(frozen=True)
class UserPersonalData:
    """
    Attributes defined for Open edX user object based on PII data.

    Arguments:
        username (str): username associated with the Open edX user.
        email (str): email associated with the Open edX user.
        name (str): email associated with the Open edX user's profile.
    """

    username = attr.ib(type=str)
    email = attr.ib(type=str)
    name = attr.ib(type=str, factory=str)


@attr.s(frozen=True)
class UserData:
    """
    Attributes defined for Open edX user object.

    Arguments:
        user_non_pii (UserNonPersonalData): user's Personal Identifiable
        Information.
        user_pii (UserPersonalData): user's Non Personal Identifiable
        Information.
    """

    user_non_pii = attr.ib(type=UserNonPersonalData)
    user_pii = attr.ib(type=UserPersonalData)


@attr.s(frozen=True)
class CourseData:
    """
    Attributes defined for Open edX Course Overview object.

    Arguments:
        course_key (str): identifier of the Course object.
        display_name (str): display name associated with the course.
        start (datetime): start date for the course.
        end (datetime): end date for the course.
    """

    course_key = attr.ib(type=CourseKey)
    display_name = attr.ib(type=str, factory=str)
    start = attr.ib(type=datetime, default=None)
    end = attr.ib(type=datetime, default=None)


@attr.s(frozen=True)
class CourseEnrollmentData:
    """
    Attributes defined for Open edX Course Enrollment object.

    Arguments:
        user (UserData): user associated with the Course Enrollment.
        course (CourseData): course where the user is enrolled in.
        mode (str): course mode associated with the course.
        is_active (bool): whether the enrollment is active.
        creation_date (datetime): creation date of the enrollment.
        created_by (UserData): if available, who created the enrollment.
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

    Arguments:
        user (UserData): user associated with the Certificate.
        course (CourseData): course where the user obtained the certificate.
        mode (str): course mode associated with the course.
        grade (str): user's grade in this course run.
        current_status (str): current certificate status.
        previous_status (str): if available, pre-event certificate status.
        download_url (str): URL where the PDF version of the certificate.
        name (str): user's name.
    """

    user = attr.ib(type=UserData)
    course = attr.ib(type=CourseData)
    mode = attr.ib(type=str)
    grade = attr.ib(type=str)
    download_url = attr.ib(type=str)
    name = attr.ib(type=str)
    current_status = attr.ib(type=str)
    previous_status = attr.ib(type=str, factory=str)


@attr.s(frozen=True)
class CohortData:
    """
    Attributes defined for Open edX Cohort Membership object.

    Arguments:
        user (UserData): user assigned to the group.
        course (CourseData): course associated with the course group.
        name (str): name of the cohort group.
    """

    user = attr.ib(type=UserData)
    course = attr.ib(type=CourseData)
    name = attr.ib(type=str)

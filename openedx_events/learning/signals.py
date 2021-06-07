"""
Custom signals definitions that representing the Open edX platform events.

All signals defined in this module must follow the name and versioning
conventions specified in docs/decisions/0002-events-naming-and-versioning.rst

They also must comply with the payload definition specified in
docs/decisions/0003-events-payload.rst
"""

from openedx_events.learning.data import (
    CertificateData,
    CohortData,
    CourseEnrollmentData,
    RegistrationFormData,
    StudentData,
)
from openedx_events.tooling import OpenEdxPublicSignal

STUDENT_REGISTRATION_COMPLETED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.student.registration.completed.v1",
    data={
        "user": StudentData,
        "registration_form": RegistrationFormData,
    }
)


SESSION_LOGIN_COMPLETED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.auth.session.login.completed.v1",
    data={
        "user": StudentData,
    }
)


COURSE_ENROLLMENT_CREATED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.course.enrollment.created.v1",
    data={
        "enrollment": CourseEnrollmentData,
    }
)


COURSE_ENROLLMENT_CHANGED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.course.enrollment.changed.v1",
    data={
        "enrollment": CourseEnrollmentData,
    }
)


COURSE_ENROLLMENT_DEACTIVATED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.course.enrollment.deactivated.v1",
    data={
        "enrollment": CourseEnrollmentData,
    }
)


CERTIFICATE_CREATED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.certificate.created.v1",
    data={
        "certificate": CertificateData,
    }
)


CERTIFICATE_CHANGED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.certificate.changed.v1",
    data={
        "certificate": CertificateData,
    }
)


CERTIFICATE_REVOKED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.certificate.revoked.v1",
    data={
        "certificate": CertificateData,
    }
)


COHORT_MEMBERSHIP_CHANGED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.cohort_membership.changed.v1",
    data={
        "cohort": CohortData,
    }
)

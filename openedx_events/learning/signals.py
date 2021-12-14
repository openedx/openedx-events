"""
Custom signals definitions that representing the Open edX platform events.

All signals defined in this module must follow the name and versioning
conventions specified in docs/decisions/0002-events-naming-and-versioning.rst

They also must comply with the payload definition specified in
docs/decisions/0003-events-payload.rst
"""

from openedx_events.learning.data import CertificateData, CohortData, CourseEnrollmentData, CourseGradeData, UserData
from openedx_events.tooling import OpenEdxPublicSignal

# .. event_type: org.openedx.learning.student.registration.completed.v1
# .. event_name: STUDENT_REGISTRATION_COMPLETED
# .. event_description: emitted when the user registration process in the LMS is completed.
# .. event_data: UserData
STUDENT_REGISTRATION_COMPLETED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.student.registration.completed.v1",
    data={
        "user": UserData,
    }
)


# .. event_type: org.openedx.learning.auth.session.login.completed.v1
# .. event_name: SESSION_LOGIN_COMPLETED
# .. event_description: emitted when the user's login process in the LMS is completed.
# .. event_data: UserData
SESSION_LOGIN_COMPLETED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.auth.session.login.completed.v1",
    data={
        "user": UserData,
    }
)


# .. event_type: org.openedx.learning.course.enrollment.created.v1
# .. event_name: COURSE_ENROLLMENT_CREATED
# .. event_description: emitted when the user's enrollment process is completed.
# .. event_data: CourseEnrollmentData
COURSE_ENROLLMENT_CREATED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.course.enrollment.created.v1",
    data={
        "enrollment": CourseEnrollmentData,
    }
)


# .. event_type: org.openedx.learning.course.enrollment.changed.v1
# .. event_name: COURSE_ENROLLMENT_CHANGED
# .. event_description: emitted when the user's enrollment update process is completed.
# .. event_data: CourseEnrollmentData
COURSE_ENROLLMENT_CHANGED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.course.enrollment.changed.v1",
    data={
        "enrollment": CourseEnrollmentData,
    }
)


# .. event_type: org.openedx.learning.course.unenrollment.completed.v1
# .. event_name: COURSE_ENROLLMENT_CHANGED
# .. event_description: emitted when the user's unenrollment process is completed.
# .. event_data: CourseEnrollmentData
COURSE_UNENROLLMENT_COMPLETED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.course.unenrollment.completed.v1",
    data={
        "enrollment": CourseEnrollmentData,
    }
)


# .. event_type: org.openedx.learning.certificate.created.v1
# .. event_name: CERTIFICATE_CREATED
# .. event_description: emitted when the user's certificate creation process is completed.
# .. event_data: CertificateData
CERTIFICATE_CREATED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.certificate.created.v1",
    data={
        "certificate": CertificateData,
    }
)


# .. event_type: org.openedx.learning.certificate.changed.v1
# .. event_name: CERTIFICATE_CHANGED
# .. event_description: emitted when the user's certificate update process is completed.
# .. event_data: CertificateData
CERTIFICATE_CHANGED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.certificate.changed.v1",
    data={
        "certificate": CertificateData,
    }
)


# .. event_type: org.openedx.learning.certificate.revoked.v1
# .. event_name: CERTIFICATE_REVOKED
# .. event_description: emitted when the user's certificate annulation process is completed.
# .. event_data: CertificateData
CERTIFICATE_REVOKED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.certificate.revoked.v1",
    data={
        "certificate": CertificateData,
    }
)


# .. event_type: org.openedx.learning.cohort_membership.changed.v1
# .. event_name: COHORT_MEMBERSHIP_CHANGED
# .. event_description: emitted when the user's cohort update is completed.
# .. event_data: CohortData
COHORT_MEMBERSHIP_CHANGED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.cohort_membership.changed.v1",
    data={
        "cohort": CohortData,
    }
)


# .. event_type: org.openedx.learning.account_settings.changed.v1
# .. event_name: ACCOUNT_SETTINGS_CHANGED
# .. event_description: emitted when the user's account settings update is completed.
# .. event_data: UserData
ACCOUNT_SETTINGS_CHANGED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.account_settings.changed.v1",
    data={
        "user": UserData,
    }
)


# .. event_type: org.openedx.learning.user.password.changed.v1
# .. event_name: PASSWORD_CHANGED
# .. event_description: emitted when the user's password update is completed.
# .. event_data: UserData
PASSWORD_CHANGED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.user.password.changed.v1",
    data={
        "user": UserData,
    }
)


# .. event_type: org.openedx.learning.user.password.changed.v1
# .. event_name: LEARNER_VERIFICATION_COMPLETED
# .. event_description: emitted when the learner's verification process is completed.
# .. event_data: UserData
LEARNER_VERIFICATION_COMPLETED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.learner.verification.completed.v1",
    data={
        "user": UserData,
    }
)


# .. event_type: org.openedx.learning.course.grade.changed.v1
# .. event_name: COURSE_GRADE_CHANGED
# .. event_description: emitted when a learner is graded.
# .. event_data: CourseGradeData, UserData
COURSE_GRADE_CHANGED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.course.grade.changed.v1",
    data={
        "course": CourseGradeData,
        "user": UserData,
    }
)


# .. event_type: org.openedx.learning.course.grade.changed.v1
# .. event_name: COURSE_GRADE_NOW_PASSED
# .. event_description: emitted when a learner has passed a course.
# .. event_data: CourseGradeData, UserData
COURSE_GRADE_NOW_PASSED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.course.grade.changed.v1",
    data={
        "course": CourseGradeData,
        "user": UserData,
    }
)


# .. event_type: org.openedx.learning.course.grade.changed.v1
# .. event_name: COURSE_GRADE_NOW_FAILED
# .. event_description: emitted when a learner has failed a course.
# .. event_data: CourseGradeData, UserData
COURSE_GRADE_NOW_FAILED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.course.grade.changed.v1",
    data={
        "course": CourseGradeData,
        "user": UserData,
    }
)

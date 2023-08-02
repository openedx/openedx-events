"""
Standardized signals definitions for events within the architecture subdomain ``learning``.

All signals defined in this module must follow the name and versioning
conventions specified in docs/decisions/0002-events-naming-and-versioning.rst

They also must comply with the payload definition specified in
docs/decisions/0003-events-payload.rst
"""

from openedx_events.learning.data import (
    CertificateData,
    CohortData,
    CourseDiscussionConfigurationData,
    CourseEnrollmentData,
    PersistentCourseGradeData,
    ProgramCertificateData,
    UserData,
    UserNotificationData,
    XBlockSkillVerificationData,
)
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
# .. event_name: COURSE_UNENROLLMENT_COMPLETED
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

# .. event_type: org.openedx.learning.program.certificate.awarded.v1
# .. event_name: PROGRAM_CERTIFICATE_AWARDED
# .. event_description: Emit when a program certificate is awarded to a learner
# .. event_data: ProgramCertificateData
PROGRAM_CERTIFICATE_AWARDED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.program.certificate.awarded.v1",
    data={
        "program_certificate": ProgramCertificateData,
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

# .. event_type: org.openedx.learning.program.certificate.revoked.v1
# .. event_name: PROGRAM_CERTIFICATE_REVOKED
# .. event_description: Emit when a program certificate is revoked from a learner
# .. event_data: ProgramCertificateData
PROGRAM_CERTIFICATE_REVOKED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.program.certificate.revoked.v1",
    data={
        "program_certificate": ProgramCertificateData,
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


# .. event_type: org.openedx.learning.discussions.configuration.changed.v1
# .. event_name: COURSE_DISCUSSIONS_CHANGED
# .. event_description: emitted when the configuration for a course's discussions changes in the course
#       Warning: This event is currently incompatible with the event bus, list/dict cannot be serialized yet
# .. event_data: CourseDiscussionConfigurationData
COURSE_DISCUSSIONS_CHANGED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.discussions.configuration.changed.v1",
    data={
        "configuration": CourseDiscussionConfigurationData
    }
)

# .. event_type: org.openedx.learning.course.persistent_grade.summary.v1
# .. event_name: PERSISTENT_GRADE_SUMMARY_CHANGED
# .. event_description: emitted when a grade changes in the course
# .. event_data: PersistentCourseGradeData
PERSISTENT_GRADE_SUMMARY_CHANGED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.course.persistent_grade_summary.changed.v1",
    data={
        "grade": PersistentCourseGradeData,
    }
)


# .. event_type: org.openedx.learning.xblock.skill.verified.v1
# .. event_name: XBLOCK_SKILL_VERIFIED
# .. event_description: Fired when an XBlock skill is verified.
# .. event_data: XBlockSkillVerificationData
XBLOCK_SKILL_VERIFIED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.xblock.skill.verified.v1",
    data={
        "xblock_info": XBlockSkillVerificationData,
    }
)

# .. event_type: org.openedx.learning.user.notification.requested.v1
# .. event_name: USER_NOTIFICATION
# .. event_description: Can be fired from apps to send user notifications.
# .. event_data: UserNotificationSendListData
# Warning: This event is currently incompatible with the event bus, list/dict cannot be serialized yet
#
USER_NOTIFICATION_REQUESTED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.user.notification.requested.v1",
    data={
        "notification_data": UserNotificationData,
    }
)

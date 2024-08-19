"""
Standardized signals definitions for events within the architecture subdomain ``learning``.

All signals defined in this module must follow the name and versioning
conventions specified in docs/decisions/0002-events-naming-and-versioning.rst

They also must comply with the payload definition specified in
docs/decisions/0003-events-payload.rst
"""

from openedx_events.learning.data import (
    BadgeData,
    CcxCoursePassingStatusData,
    CertificateData,
    CohortData,
    CourseAccessRoleData,
    CourseDiscussionConfigurationData,
    CourseEnrollmentData,
    CourseNotificationData,
    CoursePassingStatusData,
    DiscussionThreadData,
    ExamAttemptData,
    ORASubmissionData,
    PersistentCourseGradeData,
    ProgramCertificateData,
    UserData,
    UserNotificationData,
    VerificationAttemptData,
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
# .. event_key_field: user.pii.username
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
# .. event_key_field: enrollment.course.course_key
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
# .. event_key_field: certificate.course.course_key
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
# .. event_key_field: program_certificate.program.uuid
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
# .. event_key_field: certificate.course.course_key
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
# .. event_key_field: program_certificate.program.uuid
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
# .. event_key_field: xblock_info.usage_key
# .. event_description: Fired when an XBlock skill is verified.
# .. event_data: XBlockSkillVerificationData
XBLOCK_SKILL_VERIFIED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.xblock.skill.verified.v1",
    data={
        "xblock_info": XBlockSkillVerificationData,
    }
)

# .. event_type: org.openedx.learning.user.notification.requested.v1
# .. event_name: USER_NOTIFICATION_REQUESTED
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

# .. event_type: org.openedx.learning.exam.attempt.submitted.v1
# .. event_name: EXAM_ATTEMPT_SUBMITTED
# .. event_description: Emitted when an exam attempt is submitted by a learner in edx-exams.
# .. event_data: ExamAttemptData
EXAM_ATTEMPT_SUBMITTED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.exam.attempt.submitted.v1",
    data={
        "exam_attempt": ExamAttemptData,
    }
)

# .. event_type: org.openedx.learning.exam.attempt.rejected.v1
# .. event_name: EXAM_ATTEMPT_REJECTED
# .. event_description: Emitted when an exam attempt is marked rejected in edx-exams.
# .. event_data: ExamAttemptData
EXAM_ATTEMPT_REJECTED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.exam.attempt.rejected.v1",
    data={
        "exam_attempt": ExamAttemptData,
    }
)

# .. event_type: org.openedx.learning.exam.attempt.verified.v1
# .. event_name: EXAM_ATTEMPT_VERIFIED
# .. event_description: Emitted when an exam attempt is marked verified in edx-exams.
# .. event_data: ExamAttemptData
EXAM_ATTEMPT_VERIFIED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.exam.attempt.verified.v1",
    data={
        "exam_attempt": ExamAttemptData,
    }
)

# .. event_type: org.openedx.learning.exam.attempt.errored.v1
# .. event_name: EXAM_ATTEMPT_ERRORED
# .. event_description: Emitted when a learner's exam attempt errors out in edx-exams.
# .. event_data: ExamAttemptData
EXAM_ATTEMPT_ERRORED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.exam.attempt.errored.v1",
    data={
        "exam_attempt": ExamAttemptData,
    }
)

# .. event_type: org.openedx.learning.exam.attempt.reset.v1
# .. event_name: EXAM_ATTEMPT_RESET
# .. event_description: Emitted when an exam attempt is reset in edx-exams.
# .. event_data: ExamAttemptData
EXAM_ATTEMPT_RESET = OpenEdxPublicSignal(
    event_type="org.openedx.learning.exam.attempt.reset.v1",
    data={
        "exam_attempt": ExamAttemptData,
    }
)

# .. event_type: org.openedx.learning.user.course_access_role.added.v1
# .. event_name: COURSE_ACCESS_ROLE_ADDED
# .. event_key_field: course_access_role_data.course_key
# .. event_description: Emitted when a user is given a course access role.
# .. event_data: CourseAccessRoleData
COURSE_ACCESS_ROLE_ADDED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.user.course_access_role.added.v1",
    data={
        "course_access_role_data": CourseAccessRoleData,
    }
)

# .. event_type: org.openedx.learning.user.course_access_role.removed.v1
# .. event_name: COURSE_ACCESS_ROLE_REMOVED
# .. event_key_field: course_access_role_data.course_key
# .. event_description: Emitted when a course access role is removed from a user.
# .. event_data: CourseAccessRoleData
COURSE_ACCESS_ROLE_REMOVED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.user.course_access_role.removed.v1",
    data={
        "course_access_role_data": CourseAccessRoleData,
    }
)

# .. event_type: org.openedx.learning.forum.thread.created.v1
# .. event_name: FORUM_THREAD_CREATED
# .. event_description: Emitted when a new thread is created in a discussion
# .. event_data: DiscussionThreadData
#       Warning: This event is currently incompatible with the event bus, list/dict cannot be serialized yet
FORUM_THREAD_CREATED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.thread.created.v1",
    data={
        "thread": DiscussionThreadData,
    }
)

# .. event_type: org.openedx.learning.forum.thread.response.created.v1
# .. event_name: FORUM_THREAD_RESPONSE_CREATED
# .. event_description: Emitted when a new response is added to a thread
# .. event_data: DiscussionThreadData
#        Warning: This event is currently incompatible with the event bus, list/dict cannot be serialized yet
FORUM_THREAD_RESPONSE_CREATED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.response.created.v1",
    data={
        "thread": DiscussionThreadData,
    }
)

# .. event_type: org.openedx.learning.forum.thread.response.comment.created.v1
# .. event_name: FORUM_RESPONSE_COMMENT_CREATED
# .. event_description: Emitted when a new comment is added to a response
# .. event_data: DiscussionThreadData
#       Warning: This event is currently incompatible with the event bus, list/dict cannot be serialized yet
FORUM_RESPONSE_COMMENT_CREATED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.response.created.v1",
    data={
        "thread": DiscussionThreadData,
    }
)


# .. event_type: org.openedx.learning.course.notification.requested.v1
# .. event_name: COURSE_NOTIFICATION_REQUESTED
# .. event_description: Emitted when a notification is requested for a course
# .. event_data: CourseNotificationData
# Warning: This event is currently incompatible with the event bus, list/dict cannot be serialized yet
#
COURSE_NOTIFICATION_REQUESTED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.course.notification.requested.v1",
    data={
        "course_notification_data": CourseNotificationData,
    }
)


# .. event_type: org.openedx.learning.ora.submission.created.v1
# .. event_name: ORA_SUBMISSION_CREATED
# .. event_description: Emitted when a new ORA submission is created
# .. event_data: ORASubmissionData
# Warning: This event is currently incompatible with the event bus, list/dict cannot be serialized yet
ORA_SUBMISSION_CREATED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.ora.submission.created.v1",
    data={
        "submission": ORASubmissionData,
    },
)


# .. event_type: org.openedx.learning.course.passing.status.updated.v1
# .. event_name: COURSE_PASSING_STATUS_UPDATED
# .. event_description: Emitted when course grade updates.
# .. event_data: CoursePassingStatusData
COURSE_PASSING_STATUS_UPDATED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.course.passing.status.updated.v1",
    data={
        "course_passing_status": CoursePassingStatusData,
    }
)


# .. event_type: org.openedx.learning.ccx.course.passing.status.updated.v1
# .. event_name: CCX_COURSE_PASSING_STATUS_UPDATED
# .. event_description: Emitted when a CCX course grade updates.
# .. event_data: CcxCoursePassingStatusData
CCX_COURSE_PASSING_STATUS_UPDATED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.ccx.course.passing.status.updated.v1",
    data={
        "course_passing_status": CcxCoursePassingStatusData,
    }
)


# .. event_type: org.openedx.learning.badge.awarded.v1
# .. event_name: BADGE_AWARDED
# .. event_description: Emit when a badge is awarded to a learner
# .. event_data: BadgeData
BADGE_AWARDED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.badge.awarded.v1",
    data={
        "badge": BadgeData,
    }
)


# .. event_type: org.openedx.learning.badge.revoked.v1
# .. event_name: BADGE_REVOKED
# .. event_description: Emit when a badge is revoked for a learner
# .. event_data: BadgeData
BADGE_REVOKED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.badge.revoked.v1",
    data={
        "badge": BadgeData,
    }
)


# .. event_type: org.openedx.learning.idv_attempt.created.v1
# .. event_name: IDV_ATTEMPT_CREATED
# .. event_description: Emitted when a IDV attempt is created by an IDV vendor
# .. event_data: VerificationAttemptData
IDV_ATTEMPT_CREATED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.idv_attempt.created.v1",
    data={
        "idv_attempt": VerificationAttemptData,
    }
)


# .. event_type: org.openedx.learning.idv_attempt.pending.v1
# .. event_name: IDV_ATTEMPT_PENDING
# .. event_description: Emitted when a IDV attempt is marked as pending by an IDV vendor
# .. event_data: VerificationAttemptData
IDV_ATTEMPT_PENDING = OpenEdxPublicSignal(
    event_type="org.openedx.learning.idv_attempt.pending.v1",
    data={
        "idv_attempt": VerificationAttemptData,
    }
)


# .. event_type: org.openedx.learning.idv_attempt.approved.v1
# .. event_name: IDV_ATTEMPT_APPROVED
# .. event_description: Emitted when a IDV attempt is approved by an IDV vendor
# .. event_data: VerificationAttemptData
IDV_ATTEMPT_APPROVED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.idv_attempt.approved.v1",
    data={
        "idv_attempt": VerificationAttemptData,
    }
)


# .. event_type: org.openedx.learning.idv_attempt.denied.v1
# .. event_name: IDV_ATTEMPT_DENIED
# .. event_description: Emitted when a IDV attempt is denied by an IDV vendor
# .. event_data: VerificationAttemptData
IDV_ATTEMPT_DENIED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.idv_attempt.denied.v1",
    data={
        "idv_attempt": VerificationAttemptData,
    }
)

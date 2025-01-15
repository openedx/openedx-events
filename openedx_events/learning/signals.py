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
# .. event_key_field: user.pii.username
# .. event_description: Emitted when a user completes registration in Open edX.
# .. event_data: UserData
# .. event_trigger_repository: openedx/edx-platform
STUDENT_REGISTRATION_COMPLETED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.student.registration.completed.v1",
    data={
        "user": UserData,
    }
)


# .. event_type: org.openedx.learning.auth.session.login.completed.v1
# .. event_name: SESSION_LOGIN_COMPLETED
# .. event_key_field: user.pii.username
# .. event_description: Emitted when a user logs in to Open edX.
# .. event_data: UserData
# .. event_trigger_repository: openedx/edx-platform
SESSION_LOGIN_COMPLETED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.auth.session.login.completed.v1",
    data={
        "user": UserData,
    }
)


# .. event_type: org.openedx.learning.course.enrollment.created.v1
# .. event_name: COURSE_ENROLLMENT_CREATED
# .. event_key_field: enrollment.course.course_key
# .. event_description: Emitted when the user enrolls in a course.
# .. event_data: CourseEnrollmentData
# .. event_trigger_repository: openedx/edx-platform
COURSE_ENROLLMENT_CREATED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.course.enrollment.created.v1",
    data={
        "enrollment": CourseEnrollmentData,
    }
)


# .. event_type: org.openedx.learning.course.enrollment.changed.v1
# .. event_name: COURSE_ENROLLMENT_CHANGED
# .. event_key_field: enrollment.course.course_key
# .. event_description: Emitted when the enrollment for a user in a course changes.
# .. event_data: CourseEnrollmentData
# .. event_trigger_repository: openedx/edx-platform
COURSE_ENROLLMENT_CHANGED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.course.enrollment.changed.v1",
    data={
        "enrollment": CourseEnrollmentData,
    }
)


# .. event_type: org.openedx.learning.course.unenrollment.completed.v1
# .. event_name: COURSE_UNENROLLMENT_COMPLETED
# .. event_key_field: enrollment.course.course_key
# .. event_description: Emitted when the user unenrolls from a course.
# .. event_data: CourseEnrollmentData
# .. event_trigger_repository: openedx/edx-platform
COURSE_UNENROLLMENT_COMPLETED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.course.unenrollment.completed.v1",
    data={
        "enrollment": CourseEnrollmentData,
    }
)


# .. event_type: org.openedx.learning.certificate.created.v1
# .. event_name: CERTIFICATE_CREATED
# .. event_key_field: certificate.course.course_key
# .. event_description: Emitted when a certificate is created for a user.
# .. event_data: CertificateData
# .. event_trigger_repository: openedx/edx-platform
CERTIFICATE_CREATED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.certificate.created.v1",
    data={
        "certificate": CertificateData,
    }
)

# .. event_type: org.openedx.learning.program.certificate.awarded.v1
# .. event_name: PROGRAM_CERTIFICATE_AWARDED
# .. event_key_field: program_certificate.program.uuid
# .. event_description: Emitted when a program certificate is awarded to a learner.
# .. event_data: ProgramCertificateData
# .. event_trigger_repository: openedx/credentials
PROGRAM_CERTIFICATE_AWARDED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.program.certificate.awarded.v1",
    data={
        "program_certificate": ProgramCertificateData,
    }
)

# .. event_type: org.openedx.learning.certificate.changed.v1
# .. event_name: CERTIFICATE_CHANGED
# .. event_description: Emitted when the user's certificate changes.
# .. event_data: CertificateData
# .. event_trigger_repository: openedx/edx-platform
CERTIFICATE_CHANGED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.certificate.changed.v1",
    data={
        "certificate": CertificateData,
    }
)


# .. event_type: org.openedx.learning.certificate.revoked.v1
# .. event_name: CERTIFICATE_REVOKED
# .. event_key_field: certificate.course.course_key
# .. event_description: Emitted when a certificate is revoked from a user.
# .. event_data: CertificateData
# .. event_trigger_repository: openedx/edx-platform
CERTIFICATE_REVOKED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.certificate.revoked.v1",
    data={
        "certificate": CertificateData,
    }
)

# .. event_type: org.openedx.learning.program.certificate.revoked.v1
# .. event_name: PROGRAM_CERTIFICATE_REVOKED
# .. event_key_field: program_certificate.program.uuid
# .. event_description: Emit when a program certificate is revoked from a learner.
# .. event_data: ProgramCertificateData
# .. event_trigger_repository: openedx/credentials
PROGRAM_CERTIFICATE_REVOKED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.program.certificate.revoked.v1",
    data={
        "program_certificate": ProgramCertificateData,
    }
)

# .. event_type: org.openedx.learning.cohort_membership.changed.v1
# .. event_name: COHORT_MEMBERSHIP_CHANGED
# .. event_description: Emitted when a user's cohort membership changes.
# .. event_data: CohortData
# .. event_trigger_repository: openedx/edx-platform
COHORT_MEMBERSHIP_CHANGED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.cohort_membership.changed.v1",
    data={
        "cohort": CohortData,
    }
)


# .. event_type: org.openedx.learning.discussions.configuration.changed.v1
# .. event_name: COURSE_DISCUSSIONS_CHANGED
# .. event_description: Emitted when the configuration for a course's discussions changes in the course.
# .. event_warning: This event is currently incompatible with the event bus, list/dict cannot be serialized yet
# .. event_data: CourseDiscussionConfigurationData
# .. event_trigger_repository: openedx/edx-platform
COURSE_DISCUSSIONS_CHANGED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.discussions.configuration.changed.v1",
    data={
        "configuration": CourseDiscussionConfigurationData
    }
)

# .. event_type: org.openedx.learning.course.persistent_grade.summary.v1
# .. event_name: PERSISTENT_GRADE_SUMMARY_CHANGED
# .. event_description: Emitted when a course's persistent grade summary changes for a user.
# .. event_data: PersistentCourseGradeData
# .. event_trigger_repository: openedx/edx-platform
PERSISTENT_GRADE_SUMMARY_CHANGED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.course.persistent_grade_summary.changed.v1",
    data={
        "grade": PersistentCourseGradeData,
    }
)


# .. event_type: org.openedx.learning.xblock.skill.verified.v1
# .. event_name: XBLOCK_SKILL_VERIFIED
# .. event_key_field: xblock_info.usage_key
# .. event_description: Emitted when an XBlock skill is verified.
# .. event_data: XBlockSkillVerificationData
# .. event_trigger_repository: openedx/xblock-skill-tagging
XBLOCK_SKILL_VERIFIED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.xblock.skill.verified.v1",
    data={
        "xblock_info": XBlockSkillVerificationData,
    }
)

# .. event_type: org.openedx.learning.user.notification.requested.v1
# .. event_name: USER_NOTIFICATION_REQUESTED
# .. event_description: Can be emitted from apps to send user notifications.
# .. event_data: UserNotificationSendListData
# .. event_warning: This event is currently incompatible with the event bus, list/dict cannot be serialized yet
# .. event_trigger_repository: openedx/edx-platform openedx/edx-ora2
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
# .. event_trigger_repository: edx/edx-exams
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
# .. event_trigger_repository: edx/edx-exams
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
# .. event_trigger_repository: edx/edx-exams
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
# .. event_trigger_repository: edx/edx-exams
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
# .. event_trigger_repository: edx/edx-exams
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
# .. event_trigger_repository: openedx/edx-platform
COURSE_ACCESS_ROLE_REMOVED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.user.course_access_role.removed.v1",
    data={
        "course_access_role_data": CourseAccessRoleData,
    }
)

# .. event_type: org.openedx.learning.forum.thread.created.v1
# .. event_name: FORUM_THREAD_CREATED
# .. event_description: Emitted when a new thread is created in a discussion.
# .. event_data: DiscussionThreadData
# .. event_trigger_repository: openedx/edx-platform
# .. event_warning: This event is currently incompatible with the event bus, list/dict cannot be serialized yet
FORUM_THREAD_CREATED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.forum.thread.created.v1",
    data={
        "thread": DiscussionThreadData,
    }
)

# .. event_type: org.openedx.learning.forum.thread.response.created.v1
# .. event_name: FORUM_THREAD_RESPONSE_CREATED
# .. event_description: Emitted when a new response is added to a thread.
# .. event_data: DiscussionThreadData
# .. event_trigger_repository: openedx/edx-platform
# .. event_warning: This event is currently incompatible with the event bus, list/dict cannot be serialized yet
FORUM_THREAD_RESPONSE_CREATED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.forum.thread.response.created.v1",
    data={
        "thread": DiscussionThreadData,
    }
)

# .. event_type: org.openedx.learning.forum.thread.response.comment.created.v1
# .. event_name: FORUM_RESPONSE_COMMENT_CREATED
# .. event_description: Emitted when a new comment is added to a response.
# .. event_data: DiscussionThreadData
# .. event_trigger_repository: openedx/edx-platform
# .. event_warning: This event is currently incompatible with the event bus, list/dict cannot be serialized yet
FORUM_RESPONSE_COMMENT_CREATED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.forum.thread.response.comment.created.v1",
    data={
        "thread": DiscussionThreadData,
    }
)


# .. event_type: org.openedx.learning.course.notification.requested.v1
# .. event_name: COURSE_NOTIFICATION_REQUESTED
# .. event_description: Emitted when a notification is requested for a course.
# .. event_data: CourseNotificationData
# .. event_trigger_repository: openedx/edx-platform
# .. event_warning: This event is currently incompatible with the event bus, list/dict cannot be serialized yet
COURSE_NOTIFICATION_REQUESTED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.course.notification.requested.v1",
    data={
        "course_notification_data": CourseNotificationData,
    }
)


# .. event_type: org.openedx.learning.ora.submission.created.v1
# .. event_name: ORA_SUBMISSION_CREATED
# .. event_description: Emitted when a user submits an ORA assignment.
# .. event_data: ORASubmissionData
# .. event_trigger_repository: openedx/edx-ora2
# .. event_warning: This event is currently incompatible with the event bus, list/dict cannot be serialized yet
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
# .. event_trigger_repository: openedx/edx-platform
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
# .. event_trigger_repository: openedx/edx-platform
CCX_COURSE_PASSING_STATUS_UPDATED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.ccx.course.passing.status.updated.v1",
    data={
        "course_passing_status": CcxCoursePassingStatusData,
    }
)


# .. event_type: org.openedx.learning.badge.awarded.v1
# .. event_name: BADGE_AWARDED
# .. event_description: Emit when a badge is awarded to a learner.
# .. event_data: BadgeData
# .. event_trigger_repository: openedx/credentials
BADGE_AWARDED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.badge.awarded.v1",
    data={
        "badge": BadgeData,
    }
)


# .. event_type: org.openedx.learning.badge.revoked.v1
# .. event_name: BADGE_REVOKED
# .. event_description: Emit when a badge is revoked for a learner,
# .. event_data: BadgeData
# .. event_trigger_repository: openedx/credentials
BADGE_REVOKED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.badge.revoked.v1",
    data={
        "badge": BadgeData,
    }
)


# .. event_type: org.openedx.learning.idv_attempt.created.v1
# .. event_name: IDV_ATTEMPT_CREATED
# .. event_description: Emitted when an IDV attempt is created.
# .. event_data: VerificationAttemptData
# .. event_trigger_repository: openedx/edx-platform
IDV_ATTEMPT_CREATED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.idv_attempt.created.v1",
    data={
        "idv_attempt": VerificationAttemptData,
    }
)


# .. event_type: org.openedx.learning.idv_attempt.pending.v1
# .. event_name: IDV_ATTEMPT_PENDING
# .. event_description: Emitted when an IDV attempt is marked as pending.
# .. event_data: VerificationAttemptData
# .. event_trigger_repository: openedx/edx-platform
IDV_ATTEMPT_PENDING = OpenEdxPublicSignal(
    event_type="org.openedx.learning.idv_attempt.pending.v1",
    data={
        "idv_attempt": VerificationAttemptData,
    }
)


# .. event_type: org.openedx.learning.idv_attempt.approved.v1
# .. event_name: IDV_ATTEMPT_APPROVED
# .. event_description: Emitted when an IDV attempt is approved.
# .. event_data: VerificationAttemptData
# .. event_trigger_repository: openedx/edx-platform
IDV_ATTEMPT_APPROVED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.idv_attempt.approved.v1",
    data={
        "idv_attempt": VerificationAttemptData,
    }
)


# .. event_type: org.openedx.learning.idv_attempt.denied.v1
# .. event_name: IDV_ATTEMPT_DENIED
# .. event_description: Emitted when an IDV attempt is denied.
# .. event_data: VerificationAttemptData
# .. event_trigger_repository: openedx/edx-platform
IDV_ATTEMPT_DENIED = OpenEdxPublicSignal(
    event_type="org.openedx.learning.idv_attempt.denied.v1",
    data={
        "idv_attempt": VerificationAttemptData,
    }
)

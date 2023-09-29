"""
Data attributes for events within the architecture subdomain `learning`.

These attributes follow the form of attr objects specified in OEP-49 data
pattern.
"""
from datetime import datetime
from typing import List, Optional

import attr
from opaque_keys.edx.keys import CourseKey, UsageKey


@attr.s(frozen=True)
class UserNonPersonalData:
    """
    Attributes defined for Open edX user object based on non-PII data.

    Arguments:
        id (int): unique identifier for the Django User object.
        is_active (bool): indicates whether the user is active.
    """

    id = attr.ib(type=int)
    is_active = attr.ib(type=bool)


@attr.s(frozen=True)
class UserPersonalData:
    """
    Attributes defined for Open edX user object based on PII data.

    Arguments:
        username (str): username associated with the Open edX user.
        email (str): email associated with the Open edX user.
        name (str): name associated with the Open edX user's profile.
    """

    username = attr.ib(type=str)
    email = attr.ib(type=str)
    name = attr.ib(type=str, factory=str)


@attr.s(frozen=True)
class UserData(UserNonPersonalData):
    """
    Attributes defined for Open edX user object.

    This class extends UserNonPersonalData to include PII data completing the
    user object.

    Arguments:
        pii (UserPersonalData): user's Personal Identifiable Information.
    """

    pii = attr.ib(type=UserPersonalData)


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
        mode (str): course mode associated with the course enrollment.
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
        mode (str): course mode associated with the course enrollment.
        grade (str): user's grade in this course run.
        download_url (str): URL where the PDF version of the certificate.
        name (str): user's name.
        current_status (str): current certificate status.
        previous_status (str): if available, pre-event certificate status.
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


@attr.s(frozen=True)
class DiscussionTopicContext:
    """
    Attributes defined for Open edX Discussion Topic Context object.

    Context for linking the external id for a discussion topic to its associated usage key.

    Arguments:
        title (str): title of the discussion. This field is cached to improve the performance, since otherwise we'd
        need to look it up in the course structure each time.
        usage_key (str): unit location.
        group_id (Optional[int]): can be used for providers that don't internally support
        cohorting but we can emulate that with different contexts for different groups.
        external_id (str): store the commentable id that is used by cs_comments_service.
        ordering (int): represent the position of the discussion topic.
        context (dict): additional structured information about the context in
          which this topic is used, such as the section, subsection etc.
    """

    title = attr.ib(type=str)
    usage_key = attr.ib(type=UsageKey, default=None)
    group_id = attr.ib(type=Optional[int], default=None)
    external_id = attr.ib(type=str, default=None)
    ordering = attr.ib(type=int, default=None)
    context = attr.ib(type=dict, factory=dict)


@attr.s(frozen=True)
class CourseDiscussionConfigurationData:
    """
    Attributes defined for Open edX Course Discussion Configuration Data object.

    Course configuration information for discussions. Contains all the metadata
    needed to configure discussions for a course.

    Arguments:
        course_key (str): identifier of the course to which the discussion belongs.
        provider_type (str): provider type from discussion settings.
        enable_in_context (bool): indicates whether in-context discussion is enabled for the course
        enable_graded_units (bool): If enabled, discussion topics will be created for graded units as well.
        unit_level_visibility (bool): visibility for unit level.
        plugin_configuration (dict): The plugin configuration data for this context/provider.
        contexts (List[DiscussionTopicContext]): contains all the contexts for which discussion
        is to be enabled.
    """

    course_key = attr.ib(type=CourseKey)
    provider_type = attr.ib(type=str)
    enable_in_context = attr.ib(type=bool, default=True)
    enable_graded_units = attr.ib(type=bool, default=False)
    unit_level_visibility = attr.ib(type=bool, default=False)
    plugin_configuration = attr.ib(type=dict, default={})
    contexts = attr.ib(type=List[DiscussionTopicContext], factory=list)


@attr.s(frozen=True)
class PersistentCourseGradeData:
    """
    Attributes defined for Open edX PersistentCourseGrade data object.

    Arguments:
        user_id (int): identifier of the grade to which the grade belongs.
        course (CourseData): Identifier of the course to which the grade belongs.
        course_edited_timestamp (datetime): date the course was edited.
        course_version (str): version of the course.
        grading_policy_hash (str): grading policy hash of the course.
        percent_grade (float): percentage of the grade.
        letter_grade (str): grade in letter
        passed_timestamp (datetime): date the course was passed.
    """

    user_id = attr.ib(type=int)
    course = attr.ib(type=CourseData)
    course_edited_timestamp = attr.ib(type=datetime)
    course_version = attr.ib(type=str)
    grading_policy_hash = attr.ib(type=str)
    percent_grade = attr.ib(type=float)
    letter_grade = attr.ib(type=str)
    passed_timestamp = attr.ib(type=datetime)


@attr.s(frozen=True)
class XBlockSkillVerificationData:
    """
    Data needed to update verification count  of tags/skills for an XBlock.

    User feedback on whether tags/skills related to an XBlock are valid.

    Arguments:
        usage_key (UsageKey): identifier of the XBlock object.
        verified_skills (List[int]): list of verified skill ids.
        ignored_skills (List[int]): list of ignored skill ids.
    """

    usage_key = attr.ib(type=UsageKey)
    verified_skills = attr.ib(type=List[int], factory=list)
    ignored_skills = attr.ib(type=List[int], factory=list)


@attr.s(frozen=True)
class UserNotificationData:
    """
    Attributes defined for Open edX User Notification data object.

    Arguments:
        user_ids (List(int)): identifier of the user to which the notification belongs.
        notification_type (str): type of the notification.
        context (dict): additional structured information about the context in
                        which this topic is used, such as the section, subsection etc.
        content_url (str): url of the content.
        app_name (str): name of the app.
    """

    user_ids = attr.ib(type=List[int])
    notification_type = attr.ib(type=str)
    content_url = attr.ib(type=str)
    app_name = attr.ib(type=str)
    course_key = attr.ib(type=CourseKey)
    context = attr.ib(type=dict, factory=dict)


@attr.s(frozen=True)
class ProgramData:
    """
    Attributes defined for the Open edX Program data object.

    Arguments:
        uuid (str): The UUID of the program (from Course-Discovery)
        title (str): The title of the program
        program_type (str): The type slug of the program (e.g. professional, microbachelors, micromasters, etc.)
    """

    uuid = attr.ib(type=str)
    title = attr.ib(type=str)
    program_type = attr.ib(type=str)


@attr.s(frozen=True)
class ProgramCertificateData:
    """
    Attributes defined for the Open edX Program Certificate data object.

    Arguments:
        user (UserData): User associated with the Program Certificate
        program (ProgramData): Program data associated with the Program Certificate
        uuid (str): UUID of the UserCredential record in Credentials
        certificate_available_date (datetime): Optional. A DateTime describing when a learner is allowed to view the
                                                credential
        status (str): The status of the credential (e.g. `awarded` or `revoked`)
        url (str): A URL to the learner's credential
    """

    user = attr.ib(type=UserData)
    program = attr.ib(type=ProgramData)
    uuid = attr.ib(type=str)
    status = attr.ib(type=str)
    url = attr.ib(type=str)
    certificate_available_date = attr.ib(type=datetime, default=None)


@attr.s(frozen=True)
class ExamAttemptData:
    """
    Attributes defined for the Open edX Exam downstream effects.

    Note that events that use this data type:
        A. Pretain to "Special Exams", e.g. Timed or Proctored exams, and not non-timed course
        subsections that are labelled as an exam.
        B. Are only ever emitted from the newer exams backend, edx-exams, and never from the
        legacy exams backend, edx-proctoring.

    The event signals that use this data have the prefix `EXAM_`, which is equivalent to "special exam".
    We are using this as a shortened form of the prefix `SPECIAL_EXAM` to avoid confusion, as these are likely
    the only type of exams that will be of concern in the context of events/the event bus.

    Arguments:
        student_user (UserData): user object for the student to whom the exam attempt belongs
        course_key (CourseKey): identifier of the course to which the exam attempt belongs
        usage_key (UsageKey): identifier of the content that will get a exam attempt
        exam_type (str): type of exam that was taken (e.g. timed, proctored, etc.)
        requesting_user (UserData): user triggering the event (sometimes a non-learner, e.g. an instructor)
    """

    student_user = attr.ib(type=UserData)
    course_key = attr.ib(type=CourseKey)
    usage_key = attr.ib(type=UsageKey)
    exam_type = attr.ib(type=str)
    requesting_user = attr.ib(type=UserData, default=None)

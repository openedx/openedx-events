"""
Data attributes for events within the architecture subdomain `learning`.

These attributes follow the form of attr objects specified in OEP-49 data
pattern.
"""
from datetime import datetime
from typing import List, Optional

import attr
from attr.validators import in_
from ccx_keys.locator import CCXLocator
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
class CcxCourseData:
    """
    Represents data for a CCX (Custom Courses for edX) course.

    Attributes:
        ccx_course_key (CCXLocator): The unique identifier for the CCX course.
        master_course_key (CourseKey): The unique identifier for the original course from which the CCX is derived.
        display_name (str): The name of the CCX course as it should appear to users.
        coach_email (str): The email address of the coach (instructor) for the CCX course.
        start (str, optional): The start date of the CCX course. Defaults to None, indicating no specific start date.
        end (str, optional): The end date of the CCX course. Defaults to None, indicating no specific end date.
        max_students_allowed (int, optional): The maximum number of students that can enroll in the CCX course. Defaults to None, indicating no limit.
    """

    ccx_course_key = attr.ib(type=CCXLocator)
    master_course_key = attr.ib(type=CourseKey)
    display_name = attr.ib(type=str, factory=str)
    coach_email = attr.ib(type=str, factory=str)
    start = attr.ib(type=str, default=None)
    end = attr.ib(type=str, default=None)
    max_students_allowed = attr.ib(type=int, default=None)


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
        user_ids (List(int)): identifier of the users to which the notification belongs.
        notification_type (str): type of the notification.
        content_url (str): url of the content.
        app_name (str): name of the app.
        course_key (str): identifier of the Course object.
        context (dict): additional structured information about the context of the notification.
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

    For more information, please see the ADR relating to this event data:
    https://github.com/openedx/openedx-events/blob/main/docs/decisions/0013-special-exam-submission-and-review-events.rst

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


@attr.s(frozen=True)
class CourseAccessRoleData:
    """
    Attributes defined for the Open edX Course Access Role data object.

    Arguments:
        user (UserData): user associated with the CourseAccessRole.
        course_key (CourseKey): identifer of the related course object.
        org (str): identifier of the organization.
        role (str): the role of the user in the course.
    """

    user = attr.ib(type=UserData)
    org_key = attr.ib(type=str)
    course_key = attr.ib(type=CourseKey)
    role = attr.ib(type=str)


@attr.s(frozen=True)
class DiscussionThreadData:
    """
    Attributes defined for the Open edX to represent events in the Forum such as comments, responses, and threads.

    For more details on the data attributes, please see the following documentation:
    https://docs.openedx.org/en/latest/developers/references/internal_data_formats/tracking_logs/student_event_types.html#edx-forum-thread-created

    Arguments:
        anonymous (bool): indicates whether the user is anonymous.
        anonymous_to_peers (bool): indicates whether the user is anonymous to peers.
        body (str): body of the discussion thread.
        category_id (int): identifier of the category.
        category_name (str): name of the category.
        commentable_id (str): identifier of the commentable.
        group_id (int): identifier of the group.
        id (int): identifier of the discussion thread.
        team_id (int): identifier of the team.
        thread_type (str): type of the thread.
        title (str): title of the thread.
        title_truncated (bool): indicates whether the title is truncated.
        truncated (bool): indicates whether the thread is truncated.
        url (str): url of the thread.
        user (UserData): information of the user that authored the thread/comment/response.
        course_id (CourseKey): identifier of the course.
        discussion (dict): discussion data. (optional, specific to comments and responses)
        user_course_roles (List[str]): user course roles.
        user_forums_roles (List[str]): user forums roles.
        options (dict): options for the thread.
    """

    anonymous = attr.ib(type=bool)
    anonymous_to_peers = attr.ib(type=bool)
    body = attr.ib(type=str)
    category_id = attr.ib(type=int)
    category_name = attr.ib(type=str)
    commentable_id = attr.ib(type=str)
    group_id = attr.ib(type=int)
    id = attr.ib(type=int)
    team_id = attr.ib(type=int)
    thread_type = attr.ib(type=str)
    title = attr.ib(type=str)
    title_truncated = attr.ib(type=bool)
    truncated = attr.ib(type=bool)
    url = attr.ib(type=str)
    user = attr.ib(type=UserData)
    course_id = attr.ib(type=CourseKey)
    discussion = attr.ib(type=dict, factory=dict)
    user_course_roles = attr.ib(type=List[str], factory=list)
    user_forums_roles = attr.ib(type=List[str], factory=list)
    options = attr.ib(type=dict, factory=dict)


@attr.s(frozen=True)
class CourseNotificationData:
    """
    Attributes defined for Open edX Course Notification data object.

    Arguments:
        course_key (str): identifier of the Course object.
        app_name (str): name of the app requesting the course notification.
        notification_type (str): type of the notification.
        content_url (str): url of the content the notification will redirect to.
        content_context (dict): additional information related to the content of the notification.
            Notification content templates are defined in edx-platform here:
                https://github.com/openedx/edx-platform/blob/master/openedx/core/djangoapps/notifications/base_notification.py#L10

        Example of content_context for a discussion notification (new_comment_on_response):

            {
                ...,
                "content_context": {
                    "post_title": "Post Title",
                    "replier_name": "test_user",
            }

        audience_filters (dict): additional information related to the audience of the notification.
            We can have different filters on course level, such as roles, enrollments, cohorts etc.

        Example of audience_filters for a discussion notification (new_discussion_post):

            {
                ...,
                "audience_filters": {
                    "enrollment": ["verified", "audit"],
                    "role": ["discussion admin", "discussion moderator"],
            }
    """

    course_key = attr.ib(type=CourseKey)
    app_name = attr.ib(type=str)
    notification_type = attr.ib(type=str)
    content_url = attr.ib(type=str)
    content_context = attr.ib(type=dict, factory=dict)
    audience_filters = attr.ib(type=dict, factory=dict)


@attr.s(frozen=True)
class ORAFileDownloadsData:
    """
    Attributes defined to represent file downloads in an ORA submission.

    Arguments:
        download_url (str): URL to download the file.
        description (str): Description of the file.
        name (str): Name of the file.
        size (int): Size of the file.
    """

    download_url = attr.ib(type=str)
    description = attr.ib(type=str)
    name = attr.ib(type=str)
    size = attr.ib(type=int)


@attr.s(frozen=True)
class ORASubmissionData:
    """
    Attributes defined to represent event when a user submits an ORA assignment.

    Arguments:
        id (str): identifier of the ORA submission.
        file_downloads (List[ORAFileDownloadsData]): list of related files in the ORA submission.
    """

    id = attr.ib(type=str)
    file_downloads = attr.ib(type=List[ORAFileDownloadsData], factory=list)


@attr.s(frozen=True)
class CoursePassingStatusData:
    """
    Represents the event data when a user's grade crosses a grading policy threshold in a course.

    Attributes:
        user (UserData): An instance of UserData containing information about the user whose grade crossed the threshold.
        course (CourseData): An instance of CourseData containing details about the course in which the grade threshold was crossed.
        update_timestamp (datetime): The timestamp when the grade crossing event was recorded.
        grading_policy_hash (str): A hash of the course's grading policy at the time of the event, used for verifying the grading policy has not changed.
    """
    PASSING = 'passing'
    FAILING = 'failing'
    STATUSES = [PASSING, FAILING]

    status = attr.ib(type=str, validator=in_(STATUSES))
    course = attr.ib(type=CourseData)
    user = attr.ib(type=UserData)
    update_timestamp = attr.ib(type=datetime)
    grading_policy_hash = attr.ib(type=str)


@attr.s(frozen=True)
class CcxCoursePassingStatusData(CoursePassingStatusData):
    """
    Extends CoursePassingStatusData for CCX courses, specifying CCX course data.

    This class is used for events where a user's grade crosses a threshold specifically in a CCX course,
    providing a custom course attribute suited for CCX course instances.

    Attributes:
        course (CcxCourseData): An instance of CcxCourseData containing details about the CCX course in which the grade threshold was crossed.
        All other attributes are inherited from CoursePassingStatusData.
    """
    course = attr.ib(type=CcxCourseData)


@attr.s(frozen=True)
class BadgeTemplateData:
    """
    Attributes defined for Open edX badge template data object.

    Arguments:
        uuid (str): UUID of the badge template
        origin (str): type of badge template
        name (str): badge name
        description (str): badge description
        image_url (str): badge image url
    """

    uuid = attr.ib(type=str)
    origin = attr.ib(type=str)
    name = attr.ib(type=str, default=None)
    description = attr.ib(type=str, default=None)
    image_url = attr.ib(type=str, default=None)


@attr.s(frozen=True)
class BadgeData:
    """
    Attributes defined for the Open edX badge data object.

    Arguments:
        uuid (str): the UUID of the badge
        user (UserData): user associated with the badge
        template (BadgeTemplateData): badge template data
    """

    uuid = attr.ib(type=str)
    user = attr.ib(type=UserData)
    template = attr.ib(type=BadgeTemplateData)

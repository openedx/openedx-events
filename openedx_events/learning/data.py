"""
Data attributes for events within the architecture subdomain `learning`.

These attributes follow the form of attr objects specified in OEP-49 data
pattern.
"""
from datetime import datetime
from typing import List

import attr
from ccx_keys.locator import CCXLocator
from opaque_keys.edx.keys import CourseKey, UsageKey

from ..content_authoring.data import XBlockData


@attr.s(frozen=True)
class UserNonPersonalData:
    """
    Data related to a user object that does not contain personal information (PII).

    Attributes:
        id (int): unique identifier for the Django User object.
        is_active (bool): indicates whether the user is active.
    """

    id = attr.ib(type=int)
    is_active = attr.ib(type=bool)


@attr.s(frozen=True)
class UserPersonalData:
    """
    Data related to a user object that contains personal information (PII).

    Attributes:
        username (str): username associated with the user.
        email (str): email associated with the user.
        name (str): name associated with the user's profile.
    """

    username = attr.ib(type=str)
    email = attr.ib(type=str)
    name = attr.ib(type=str, factory=str)


@attr.s(frozen=True)
class UserData(UserNonPersonalData):
    """
    Data related to a user object, including personal information and non-personal information.

    This class extends UserNonPersonalData to include PII data completing the user object.

    Attributes:
        id (int): unique identifier for the Django User object.
        is_active (bool): indicates whether the user is active.
        pii (UserPersonalData): user's Personal Identifiable Information.
    """

    pii = attr.ib(type=UserPersonalData)


@attr.s(frozen=True)
class CourseData:
    """
    Data related to a course object.

    This data is based on the fields available in the CourseOverview data model
    defined in the course_overviews app.

    Attributes:
        course_key (str): identifier of the course.
        display_name (str): display name associated with the course.
        start (datetime): start date for the course. Defaults to None.
        end (datetime): end date for the course. Defaults to None.
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
        max_students_allowed (int, optional): The maximum number of students that can enroll in the CCX course.
           Defaults to None, indicating no limit.
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
    Data related to a course enrollment object.

    This data is based on the fields available in the CourseEnrollment data model
    defined in the student app.

    Attributes:
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
    Data related to a certificate object.

    This data is based on the GeneratedCertificate data model defined in the
    certificates app.

    Attributes:
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
    Attributes defined for cohort membership object.

    This data is based on the fields available in the CohortMembership data model
    defined in the cohorts app.

    Attributes:
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
    Data related to a discussion topic context.

    Context for linking the external id for a discussion topic to its associated usage key.

    Attributes:
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
    group_id = attr.ib(type=int, default=None)
    external_id = attr.ib(type=str, default=None)
    ordering = attr.ib(type=int, default=None)
    context = attr.ib(type=dict[str, str], factory=dict)


@attr.s(frozen=True)
class CourseDiscussionConfigurationData:
    """
    Data related to a course discussion configuration object.

    Course configuration information for discussions. Contains all the metadata
    needed to configure discussions for a course.

    Attributes:
        course_key (str): identifier of the course to which the discussion belongs.
        provider_type (str): provider type from discussion settings.
        enable_in_context (bool): indicates whether in-context discussion is enabled for the course
        enable_graded_units (bool): If enabled, discussion topics will be created for graded units as well.
        unit_level_visibility (bool): visibility for unit level.
        plugin_configuration (dict): The plugin configuration data for this context/provider.
        contexts (List[DiscussionTopicContext]): contains all the contexts for which discussion is to be enabled.
    """

    course_key = attr.ib(type=CourseKey)
    provider_type = attr.ib(type=str)
    enable_in_context = attr.ib(type=bool, default=True)
    enable_graded_units = attr.ib(type=bool, default=False)
    unit_level_visibility = attr.ib(type=bool, default=False)
    plugin_configuration = attr.ib(type=dict[str, bool], default=dict)
    contexts = attr.ib(type=List[DiscussionTopicContext], factory=list)


@attr.s(frozen=True)
class PersistentCourseGradeData:
    """
    Data related to a persistent course grade object.

    This data is based on the fields available in the PersistentCourseGrade data model
    defined in the grades app.

    Attributes:
        user_id (int): identifier of the user to which the grade belongs.
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
class XBlockWithScoringData(XBlockData):
    """
    A subclass of XBlockData that includes scoring related information.
    """
    weight = attr.ib(float)
    raw_possible = attr.ib(float)
    graded = attr.ib(bool)


@attr.s(frozen=True)
class PersistentSubsectionGradeData:
    """
    Data related to a persistent subsection grade object.

    This data is based on the fields available in the PersistentSubsectionGrade
    data model defined in the openedx-platform grades app.

    Attributes:
        user_id (int): identifier of the user to which the grade belongs.
        course (CourseData): Identifier of the course to which the grade belongs.
        subsection_edited_timestamp (datetime): date the subsection was edited.
        grading_policy_hash (str): grading policy hash of the course.
        usage_key (UsageKey): UsageKey of the subsection being graded.
    """
    user_id = attr.ib(type=int)
    course = attr.ib(type=CourseData)
    subsection_edited_timestamp = attr.ib(type=datetime)
    grading_policy_hash = attr.ib(type=str)

    usage_key = attr.ib(type=UsageKey)

    # The "graded" attribute can be set on individual problems if desired, so
    # this is what's supposed to count towards their progress page/grades. Other
    # ungraded problems may exist (e.g. practice problems). In practice, this
    # will almost never happen because marking individual problems as ungraded
    # requires manually editing XML via import or the advanced editor.
    # Regardless, if you want to answer the question of, "What did the user earn
    # for this assignment?", use these fields.
    weighted_graded_earned = attr.ib(type=float)
    weighted_graded_possible = attr.ib(type=float)

    # This represents the earned/possible for all XBlock types that are capable
    # of holding scoring data in this subsection, regardless of whether they are
    # marked as "graded" or not, i.e. regardless of whether these points count
    # towards the student's progress page and final grade. This may have some
    # obscure use cases, like if for some reason you want to judge mastery based
    # on an assignment that does not actually count towards the grade of the
    # course it's in. Overall, this is just here to ensure parity with the
    # pre-existing event emitted by openedx-platform.
    weighted_total_earned = attr.ib(type=float)
    weighted_total_possible = attr.ib(type=float)

    first_attempted = attr.ib(type=datetime)

    # Every user may see a slightly different permutation of subsection content
    # depending on various dynamic block types like LibraryContentBlock, as well
    # access rules like cohorts and enrollment tracks. A student can only be
    # graded on what they have access to, so the total possible grade may vary
    # from student to student. The visible_blocks attribute captures all the
    # blocks that were available to this user at the time their subsection grade
    # was updated.
    visible_blocks = attr.ib(type=List[XBlockWithScoringData])
    visible_blocks_hash = attr.ib(type=str)


@attr.s(frozen=True)
class XBlockSkillVerificationData:
    """
    Data needed to update verification count of tags/skills for an XBlock.

    User feedback on whether tags/skills related to an XBlock are valid.

    Attributes:
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
    Data related to a user notification object.

    Attributes:
        user_ids (List[int]): identifier of the users to which the notification belongs.
        notification_type (str): type of the notification.
        content_url (str): url of the content.
        app_name (str): name of the app.
        course_key (CourseKey): identifier of the Course object.
        context (dict[str, str]): additional structured information about the context of the notification.
    """

    user_ids = attr.ib(type=List[int])
    notification_type = attr.ib(type=str)
    content_url = attr.ib(type=str)
    app_name = attr.ib(type=str)
    course_key = attr.ib(type=CourseKey)
    context = attr.ib(type=dict[str, str], factory=dict)


@attr.s(frozen=True)
class ProgramData:
    """
    Data related to a program object.

    Attributes:
        uuid (str): The UUID of the program (from Course-Discovery).
        title (str): The title of the program.
        program_type (str): The type slug of the program (e.g. professional, microbachelors, micromasters, etc.).
    """

    uuid = attr.ib(type=str)
    title = attr.ib(type=str)
    program_type = attr.ib(type=str)


@attr.s(frozen=True)
class ProgramCertificateData:
    """
    Data related to a Program Certificate object.

    Attributes:
        user (UserData): User associated with the Program Certificate.
        program (ProgramData): Program data associated with the Program Certificate.
        uuid (str): UUID of the UserCredential record in Credentials.
        certificate_available_date (datetime): Optional. A DateTime describing when a learner is allowed to view the
           credential.
        status (str): The status of the credential (e.g. `awarded` or `revoked`).
        url (str): A URL to the learner's credential.
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
    Data for the Open edX Exam downstream effects.

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

    Attributes:
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
    Data related to a user's access role in a course.

    Attributes:
        user (UserData): user associated with the CourseAccessRole.
        course_key (CourseKey): identifier of the related course object.
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
    Data related to a discussion thread object, used to represent Forum events such as comments, responses, and threads.

    For more details on the data attributes, please see the following documentation:
    https://docs.openedx.org/en/latest/developers/references/internal_data_formats/tracking_logs/student_event_types.html#edx-forum-thread-created

    Attributes:
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

    body = attr.ib(type=str)
    commentable_id = attr.ib(type=str)
    id = attr.ib(type=str)
    truncated = attr.ib(type=bool)
    url = attr.ib(type=str)
    user = attr.ib(type=UserData)
    course_id = attr.ib(type=CourseKey)
    thread_type = attr.ib(type=str, default=None)
    anonymous = attr.ib(type=bool, default=None)
    anonymous_to_peers = attr.ib(type=bool, default=None)
    title = attr.ib(type=str, default=None)
    title_truncated = attr.ib(type=bool, default=None)
    group_id = attr.ib(type=int, default=None)
    team_id = attr.ib(type=int, default=None)
    category_id = attr.ib(type=int, default=None)
    category_name = attr.ib(type=str, default=None)
    discussion = attr.ib(type=dict[str, str], default=None)
    user_course_roles = attr.ib(type=List[str], factory=list)
    user_forums_roles = attr.ib(type=List[str], factory=list)
    options = attr.ib(type=dict[str, bool], factory=dict)


@attr.s(frozen=True)
class CourseNotificationData:
    """
    Data related to a course notification object.

    Attributes:
        course_key (str): identifier of the Course object.
        app_name (str): name of the app requesting the course notification.
        notification_type (str): type of the notification.
        content_url (str): url of the content the notification will redirect to.
        content_context (dict[str, str]): additional information related to the content of the notification.
           Notification content templates are defined in edx-platform here:
           https://github.com/openedx/edx-platform/blob/master/openedx/core/djangoapps/notifications/base_notification.py#L10
        audience_filters (dict[str, list[str]]): additional information related to the audience of the notification.
           We can have different filters on course level, such as roles, enrollments, cohorts etc.

    Example of content_context for a discussion notification:

        >>> {
            ...,
            "content_context": {
                "post_title": "Post Title",
                "replier_name": "test_user",
        }


    Example of audience_filters for a discussion notification (new_discussion_post):

        >>> {
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
    content_context = attr.ib(type=dict[str, str], factory=dict)
    audience_filters = attr.ib(type=dict[str, List[str]], factory=dict)


@attr.s(frozen=True)
class ORASubmissionAnswer:
    """
    Data related to the answer submitted by the user in an ORA submission.

    Attributes:
        parts (List[dict]): List with the response text in the ORA submission.

        The following attributes are used to represent the files submitted in the ORA submission:

        file_keys (List[str]): List of file keys in the ORA submission.
        file_descriptions (List[str]): List of file descriptions in the ORA submission.
        file_names (List[str]): List of file names in the ORA submission.
        file_sizes (List[int]): List of file sizes in the ORA submission.
        file_urls (List[str]): List of file URLs in the ORA submission.
    """

    parts = attr.ib(type=List[dict[str, str]], factory=list)
    file_keys = attr.ib(type=List[str], factory=list)
    file_descriptions = attr.ib(type=List[str], factory=list)
    file_names = attr.ib(type=List[str], factory=list)
    file_sizes = attr.ib(type=List[int], factory=list)
    file_urls = attr.ib(type=List[str], factory=list)


@attr.s(frozen=True)
class ORASubmissionData:
    """
    Data associated to the ORA assessment submitted by a user.

    Attributes:
        uuid (str): The UUID of the ORA submission.
        anonymous_user_id (str): Optional. Anonymous user ID of the user who submitted the ORA submission.
        location (str): Optional. Location of the ORA submission.
        attempt_number (int): Attempt number of the ORA submission.
        created_at (datetime): Date and time when the ORA submission was created.
        submitted_at (datetime): Date and time when the ORA submission was submitted.
        answer (ORASubmissionAnswer): Answer submitted by the user in the ORA submission.
    """

    uuid = attr.ib(type=str)
    anonymous_user_id = attr.ib(type=str)
    location = attr.ib(type=str)
    attempt_number = attr.ib(type=int)
    created_at = attr.ib(type=datetime)
    submitted_at = attr.ib(type=datetime)
    answer = attr.ib(type=ORASubmissionAnswer)


@attr.s(frozen=True)
class CoursePassingStatusData:
    """
    Represents the event data when a user's grade is updated, indicates if current grade is enough for course passing.

    Attributes:
        is_passing (bool): Indicates whether the user's grade is enough to pass the course.
        user (UserData): An instance of UserData containing information about the user whose grade was updated.
        course (CourseData): An instance of CourseData containing details about the course
           in which the grade was updated.
    """

    is_passing = attr.ib(type=bool)
    course = attr.ib(type=CourseData)
    user = attr.ib(type=UserData)


@attr.s(frozen=True)
class CcxCoursePassingStatusData(CoursePassingStatusData):
    """
    Extends CoursePassingStatusData for CCX courses, specifying CCX course data.

    This class is used for events where a user's grade crosses a threshold specifically in a CCX course,
    providing a custom course attribute suited for CCX course instances.

    Attributes:
        course (CcxCourseData): An instance of CcxCourseData containing details about the CCX course
           in which the grade threshold was crossed.

        All other attributes are inherited from CoursePassingStatusData.
    """

    course = attr.ib(type=CcxCourseData)


@attr.s(frozen=True)
class BadgeTemplateData:
    """
    Data related to a badge template object.

    Attributes:
        uuid (str): UUID of the badge template.
        origin (str): type of badge template.
        name (str): badge name.
        description (str): badge description.
        image_url (str): badge image url.
    """

    uuid = attr.ib(type=str)
    origin = attr.ib(type=str)
    name = attr.ib(type=str, default=None)
    description = attr.ib(type=str, default=None)
    image_url = attr.ib(type=str, default=None)


@attr.s(frozen=True)
class BadgeData:
    """
    Data related to a badge object.

    Attributes:
        uuid (str): the UUID of the badge.
        user (UserData): user associated with the badge.
        template (BadgeTemplateData): badge template data.
    """

    uuid = attr.ib(type=str)
    user = attr.ib(type=UserData)
    template = attr.ib(type=BadgeTemplateData)


@attr.s(frozen=True)
class VerificationAttemptData:
    """
    Data related to a IDV attempt object.

    Attributes:
        attempt_id (int): the id of the verification attempt
        user (User): the user (usually a learner) performing the verification attempt.
        status (string): the status of the verification attempt.
        name (string): the name being ID verified. Defaults to None.
        expiration_datetime (datetime, optional): When the verification attempt expires. Defaults to None.
    """

    attempt_id = attr.ib(type=int)
    user = attr.ib(type=UserData)
    status = attr.ib(type=str)
    name = attr.ib(type=str, default=None)
    expiration_date = attr.ib(type=datetime, default=None)


@attr.s(frozen=True)
class ExternalGraderScoreData:
    """
    Class that encapsulates score data provided by an external grader.

    This class uses attr.s with frozen=True to create an immutable structure
    containing information about the score assigned to a student submission.

    Attributes:
        points_possible (int): Maximum possible score for this assignment
        points_earned (int): Score earned by the student
        course_id (str): Unique identifier for the course
        score_msg (str): Descriptive message about the score (feedback)
        submission_id (int): Unique identifier for the graded submission
        user_id (str): ID of the user who submitted the assignment
        module_id (str): ID of the module/problem being graded
        queue_key (str): Unique key for the submission in the queue
        queue_name (str): Name of the queue that processed the submission
    """

    points_possible = attr.ib(type=int)
    points_earned = attr.ib(type=int)
    course_id = attr.ib(type=str)
    score_msg = attr.ib(type=str)
    submission_id = attr.ib(type=int)
    user_id = attr.ib(type=str)
    module_id = attr.ib(type=str)
    queue_key = attr.ib(type=str)
    queue_name = attr.ib(type=str)


@attr.s(frozen=True)
class LtiProviderLaunchParamsData:
    """
    Data required for a successful LTI launch.

    Attributes:
        roles (str): A comma-separated list of roles (as per LTI Spec) of the User.
        context_id (str): An ID for the launch context of LTI content.
        user_id (str): External (LTI) User ID of user performing the launch.
        extra_params (dict): A dictionary of other optional launch parameters.
    """
    roles = attr.ib(type=str)
    context_id = attr.ib(type=str)
    user_id = attr.ib(type=str)
    extra_params = attr.ib(type=dict[str, str], factory=dict)


@attr.s(frozen=True)
class LtiProviderLaunchData:
    """
    Class that encapsulates LTI data for an LTI launch event.

    Attributes:
        user (UserData): The user data for the Open edX user initiating the launch.
        course_key (CourseKey): The unique course ID for the course to which the launched content belongs.
        usage_key (UsageKey): The usage key for the content being luanched via LtiProviderLaunchParamsData.
        launch_params (LtiProviderLaunchParamsData): The LTI parameters used for the launch.
    """
    user = attr.ib(type=UserData)
    course_key = attr.ib(type=CourseKey)
    usage_key = attr.ib(type=UsageKey)
    launch_params = attr.ib(type=LtiProviderLaunchParamsData)

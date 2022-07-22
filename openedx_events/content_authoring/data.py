"""
Data attributes for events within the architecture subdomain ``content_authoring``.

These attributes follow the form of attr objects specified in OEP-49 data
pattern.
"""
from datetime import datetime

import attr
from opaque_keys.edx.keys import CourseKey


@attr.s(frozen=True)
class VideoData:
    """
    Data for a media object (image or video).

    Arguments:
        uri (str): media object filename
        uri_absolute (str): fully qualified media object location
    """

    uri = attr.ib(type=str, default=None)
    uri_absolute = attr.ib(type=str, default=None)


@attr.s(frozen=True)
class ImageData:
    """
    Data for a display image at multiple sizes.

    Arguments:
        uri_raw (str): relative uri of the raw image (required)
        uri_absolute_raw (str): absolute uri of the raw image (optional)
        uri_small (str): relative uri of a small version of the image (optional)
        uri_absolute_small (str): absolute uri of a small version of the image (optional)
        uri_large (str): relative uri of a large version of the image (optional)
        uri_absolute_large (str): absolute uri of a large version of the image (optional)
    """

    uri_raw = attr.ib(type=str)
    uri_absolute_raw = attr.ib(type=str, default=None)
    uri_small = attr.ib(type=str, default=None)
    uri_absolute_small = attr.ib(type=str, default=None)
    uri_large = attr.ib(type=str, default=None)
    uri_absolute_large = attr.ib(type=str, default=None)


@attr.s(frozen=True)
class CourseMediaData:
    """
    Data describing media for the course catalog display.

    Arguments:
        banner_image (ImageData): top banner image (optional)
        course_image (ImageData): catalog image (optional)
        course_video (VideoData): catalog video (optional)
        course_card_image (ImageData): course card image (optional)
    """

    banner_image = attr.ib(type=ImageData, default=None)
    course_image = attr.ib(type=ImageData, default=None)
    course_video = attr.ib(type=VideoData, default=None)
    course_card_image = attr.ib(type=ImageData, default=None)


@attr.s(frozen=True)
class CourseScheduleData:
    """
    Data describing course scheduling.

    Arguments:
        start (str): course start date
        end (str): course end date
        pacing (str): 'instructor' or 'self'
        enrollment_start (datetime): start of course enrollment (optional)
        enrollment_end (datetime): end of course enrollment (optional)
    """

    start = attr.ib(type=datetime)
    end = attr.ib(type=datetime)
    pacing = attr.ib(type=str)
    enrollment_start = attr.ib(type=datetime, default=None)
    enrollment_end = attr.ib(type=datetime, default=None)


@attr.s(frozen=True)
class CourseCatalogData:
    """
    Data needed for a course catalog entry.

    Arguments:
        course_key (CourseKey): identifier of the Course object.
        name (str): course name
        org (str): course organization identifier
        number (str): course number
        short_description (str): one- or two-sentence course description (optional)
        display_name (str): display name associated with the course.
        effort (str): estimated level of effort in hours per week (optional). Kept as a str to align with the lms model.
        schedule_data (CourseScheduleData): scheduling information for the course
        media (CourseMediaData): associated media for the course (video and images)
        hidden (bool): whether the course is hidden from search
        invitation_only (bool): whether the course requires an invitation to enroll
        blocks_url (str): URL of the course blocks resource
    """

    # basic identifiers
    id = attr.ib(type=CourseKey)
    course_id = attr.ib(type=CourseKey)
    name = attr.ib(type=str)
    number = attr.ib(type=str)
    org = attr.ib(type=str)

    # additional marketing information
    short_description = attr.ib(type=str, default=None)
    effort = attr.ib(type=str, default=None)
    display_name = attr.ib(type=str, default=None)
    schedule_data = attr.ib(type=CourseScheduleData, default=None)
    media = attr.ib(type=CourseMediaData, default=None)
    hidden = attr.ib(type=bool, default=False)
    invitation_only = attr.ib(type=bool, default=False)
    blocks_url = attr.ib(type=str, default=None)

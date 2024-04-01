"""
Data attributes for events within the architecture subdomain ``content_authoring``.

These attributes follow the form of attr objects specified in OEP-49 data
pattern.

The attributes for the events come from the CourseDetailView in the LMS, with some unused fields removed
(see deprecation proposal at https://github.com/openedx/public-engineering/issues/160)
"""
from datetime import datetime
from typing import BinaryIO, List

import attr
from opaque_keys.edx.keys import CourseKey, UsageKey
from opaque_keys.edx.locator import LibraryLocatorV2, LibraryUsageLocatorV2


@attr.s(frozen=True)
class CourseData:
    """
    Attributes defined for Open edX Course object.

    Arguments:
        course_key (CourseKey): identifier of the Course object.
    """

    course_key = attr.ib(type=CourseKey)


@attr.s(frozen=True)
class CourseScheduleData:
    """
    Data describing course scheduling.

    Arguments:
        start (datetime): course start date
        pacing (str): 'instructor' or 'self'
        end (datetime): course end date (optional)
        enrollment_start (datetime): start of course enrollment (optional)
        enrollment_end (datetime): end of course enrollment (optional)
    """

    start = attr.ib(type=datetime)
    pacing = attr.ib(type=str)
    end = attr.ib(type=datetime, default=None)
    enrollment_start = attr.ib(type=datetime, default=None)
    enrollment_end = attr.ib(type=datetime, default=None)


@attr.s(frozen=True)
class CourseCatalogData:
    """
    Data needed for a course catalog entry.

    Arguments:
        course_key (CourseKey): identifier of the Course object.
        name (str): course name
        schedule_data (CourseScheduleData): scheduling information for the course
        hidden (bool): whether the course is hidden from search (optional)
        invitation_only (bool): whether the course requires an invitation to enroll
    """

    # basic identifiers
    course_key = attr.ib(type=CourseKey)
    name = attr.ib(type=str)

    # additional marketing information
    schedule_data = attr.ib(type=CourseScheduleData)
    hidden = attr.ib(type=bool, default=False)
    invitation_only = attr.ib(type=bool, default=False)


@attr.s(frozen=True)
class XBlockData:
    """
    Data about changed XBlock.

    Arguments:
        usage_key (UsageKey): identifier of the XBlock object.
        block_type (str): type of block.
        version (UsageKey): identifier of the XBlock object with branch and version data (optional). This
        could be used to get the exact version of the XBlock object.
    """

    usage_key = attr.ib(type=UsageKey)
    block_type = attr.ib(type=str)
    version = attr.ib(type=UsageKey, default=None, kw_only=True)


@attr.s(frozen=True)
class DuplicatedXBlockData(XBlockData):
    """
    Data about duplicated XBlock.

    This class extends XBlockData to include source_usage_key.

    Arguments:
        source_usage_key (UsageKey): identifier of the source XBlock object.
    """

    source_usage_key = attr.ib(type=UsageKey)


@attr.s(frozen=True)
class CertificateSignatoryData:
    """
    Attributes defined for Open edX CertificateSignatory data object.

    Arguments:
        image (BinaryIO): certificate signature image.
        name (str): name of signatory.
        organization (str): organization that signatory belongs to.
        title (int): signatory title.
    """

    # Note: Please take care that the image field is BinaryIO, which means
    # that a file can be passed as an array of bytes. Watch the size of this file.
    # It can potentially be large, making it difficult to pass this data structure through the Event Bus
    # (CloudEvent messages, which should be 64K or less) and store it on disk space.
    # We suggest referring to MAX_ASSET_UPLOAD_FILE_SIZE_IN_MB, i.e. restriction in the Studio for such cases.
    image = attr.ib(type=BinaryIO)
    # end Note
    name = attr.ib(type=str)
    organization = attr.ib(type=str)
    title = attr.ib(type=str)


@attr.s(frozen=True)
class CertificateConfigData:
    """
    Attributes defined for Open edX CertificateConfig data object.

    Arguments:
        certificate_type (str): certificate type. Possible types are certificate relevant course modes:
         - credit,
         - verified,
         - professional,
         - no-id-professional,
         - executive-education,
         - paid-executive-education,
         - paid-bootcamp,
         - masters.
        course_key (CourseKey): identifier of the Course object.
        title (str): certificate title.
        signatories (List[CertificateSignatoryData]): contains a collection of signatures
        that belong to the certificate configuration.
        is_active (bool): indicates whether the certifivate configuration is active.
    """

    certificate_type = attr.ib(type=str)
    course_key = attr.ib(type=CourseKey)
    title = attr.ib(type=str)
    signatories = attr.ib(type=List[CertificateSignatoryData], factory=list)
    is_active = attr.ib(type=bool, default=False)


@attr.s(frozen=True)
class ContentLibraryData:
    """
    Data about changed ContentLibrary.

    Arguments:
        library_key (LibraryLocatorV2): a key that represents a Blockstore-based content library.
        update_blocks (bool): flag that indicates whether the content library blocks indexes should be updated
    """

    library_key = attr.ib(type=LibraryLocatorV2)
    update_blocks = attr.ib(type=bool, default=False)


@attr.s(frozen=True)
class LibraryBlockData:
    """
    Data about changed LibraryBlock.

    Arguments:
        library_key (LibraryLocatorV2): a key that represents a Blockstore-based content library.
        usage_key (LibraryUsageLocatorV2): a key that represents a XBlock in a Blockstore-based content library.
    """

    library_key = attr.ib(type=LibraryLocatorV2)
    usage_key = attr.ib(type=LibraryUsageLocatorV2)


@attr.s(frozen=True)
class ContentObjectData:
    """
    Data about changed content object

    Arguments:
        object_id (str): identifier of the Content object. This represents the id of the course or library block
        as a string. For example:
        block-v1:SampleTaxonomyOrg2+STC1+2023_1+type@vertical+block@f8de78f0897049ce997777a3a31b6ea0
    """

    object_id = attr.ib(type=str)

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
from opaque_keys.edx.locator import LibraryCollectionLocator, LibraryLocatorV2, LibraryUsageLocatorV2


@attr.s(frozen=True)
class CourseData:
    """
    Data related to a course object.

    Attributes:
        course_key (CourseKey): identifier of the Course object.
    """

    course_key = attr.ib(type=CourseKey)


@attr.s(frozen=True)
class CourseScheduleData:
    """
    Data related to a course schedule.

    Attributes:
        start (datetime): course start date.
        pacing (str): 'instructor' or 'self'.
        end (datetime): course end date (optional).
        enrollment_start (datetime): start of course enrollment (optional).
        enrollment_end (datetime): end of course enrollment (optional).
    """

    start = attr.ib(type=datetime)
    pacing = attr.ib(type=str)
    end = attr.ib(type=datetime, default=None)
    enrollment_start = attr.ib(type=datetime, default=None)
    enrollment_end = attr.ib(type=datetime, default=None)


@attr.s(frozen=True)
class CourseCatalogData:
    """
    Data related to a course catalog entry.

    Attributes:
        course_key (CourseKey): identifier of the Course object.
        name (str): course name.
        schedule_data (CourseScheduleData): scheduling information for the course.
        hidden (bool): whether the course is hidden from search (optional).
        invitation_only (bool): whether the course requires an invitation to enroll.
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
    Data related to an XBlock object.

    Attributes:
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
    Data related to an XBlock object that has been duplicated.

    This class extends XBlockData to include source_usage_key.

    Attributes:
        source_usage_key (UsageKey): identifier of the source XBlock object.
    """

    source_usage_key = attr.ib(type=UsageKey)


@attr.s(frozen=True)
class CertificateSignatoryData:
    """
    Data related to a certificate signatory. Subset of CertificateSignatory object from the LMS.

    Attributes:
        image (BinaryIO): certificate signature image. Take care that the image field is BinaryIO.
        name (str): name of signatory.
        organization (str): organization that signatory belongs to.
        title (str): signatory title.
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
    Data related to a certificate configuration. Subset of CertificateConfig object from the LMS.

    Attributes:
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
    Data related to a content library that has changed.

    Attributes:
        library_key (LibraryLocatorV2): a key that represents a Blockstore-based content library.
        update_blocks (bool): flag that indicates whether the content library blocks indexes should be updated.
    """

    library_key = attr.ib(type=LibraryLocatorV2)
    update_blocks = attr.ib(type=bool, default=False)


@attr.s(frozen=True)
class LibraryBlockData:
    """
    Data related to a library block that has changed.

    Attributes:
        library_key (LibraryLocatorV2): a key that represents a Blockstore-based content library.
        usage_key (LibraryUsageLocatorV2): a key that represents a XBlock in a Blockstore-based content library.
    """

    library_key = attr.ib(type=LibraryLocatorV2)
    usage_key = attr.ib(type=LibraryUsageLocatorV2)


@attr.s(frozen=True)
class ContentObjectData:
    """
    Data related to a content object.

    Attributes:
        object_id (str): identifier of the Content object. This represents the id of the course or library block
           as a string. For example:
           >>> block-v1:SampleTaxonomyOrg2+STC1+2023_1+type@vertical+block@f8de78f0897049ce997777a3a31b6ea0
    """

    object_id = attr.ib(type=str)


@attr.s(frozen=True)
class ContentObjectChangedData(ContentObjectData):
    """
    Data related to a content object that has changed.

    Attributes:
        object_id (str): identifier of the Content object. This represents the id of the course or library block
           as a string. For example:
           >>> block-v1:SampleTaxonomyOrg2+STC1+2023_1+type@vertical+block@f8de78f0897049ce997777a3a31b6ea0
        changes: list of changes made to this ContentObject, e.g. "tags", "collections". If list is empty,
           assume everything has changed.
    """

    changes = attr.ib(type=List[str], factory=list)


@attr.s(frozen=True)
class LibraryCollectionData:
    """
    Data related to a library collection that has changed.

    Attributes:
        collection_key (LibraryCollectionLocator): identifies the collection within the library's learning package
        background (bool): indicate whether the sender doesn't want to wait for handler to finish execution,
           i.e., the handler can run the task in background. By default it is False.
    """

    collection_key = attr.ib(type=LibraryCollectionLocator)
    background = attr.ib(type=bool, default=False)


@attr.s(frozen=True)
class LibraryContainerData:
    """
    Data related to a library container that has changed.

    Attributes:
        library_key (LibraryLocatorV2): a key that represents a content library.
        container_key (str): identifies the container within the library's learning package (e.g.  unit, section)
        background (bool): indicate whether the sender doesn't want to wait for handler to finish execution,
           i.e., the handler can run the task in background. By default it is False.
    """

    library_key = attr.ib(type=LibraryLocatorV2)
    container_key = attr.ib(type=str)
    background = attr.ib(type=bool, default=False)

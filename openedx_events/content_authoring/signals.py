"""
Standardized signals definitions for events within the architecture subdomain ``content_authoring``.

All signals defined in this module must follow the name and versioning
conventions specified in OEP-41.

They also must comply with the payload definition specified in
docs/decisions/0003-events-payload.rst
"""
from openedx_events.content_authoring.data import (
    CertificateConfigData,
    ContentLibraryData,
    ContentObjectData,
    CourseCatalogData,
    CourseData,
    DuplicatedXBlockData,
    LibraryBlockData,
    XBlockData,
)
from openedx_events.tooling import OpenEdxPublicSignal

# .. event_type: org.openedx.content_authoring.course.catalog_info.changed.v1
# .. event_name: COURSE_CATALOG_INFO_CHANGED
# .. event_key_field: catalog_info.course_key
# .. event_description: Fired when a course changes in Studio in a way that is relevant for catalog consumers.
# .. event_data: CourseCatalogData
COURSE_CATALOG_INFO_CHANGED = OpenEdxPublicSignal(
    event_type="org.openedx.content_authoring.course.catalog_info.changed.v1",
    data={
        "catalog_info": CourseCatalogData,
    }
)

# .. event_type: org.openedx.content_authoring.xblock.created.v1
# .. event_name: XBLOCK_CREATED
# .. event_key_field: xblock_info.usage_key
# .. event_description: Fired when an XBlock is created.
# .. event_data: XBlockData
XBLOCK_CREATED = OpenEdxPublicSignal(
    event_type="org.openedx.content_authoring.xblock.created.v1",
    data={
        "xblock_info": XBlockData,
    }
)

# .. event_type: org.openedx.content_authoring.xblock.updated.v1
# .. event_name: XBLOCK_UPDATED
# .. event_key_field: xblock_info.usage_key
# .. event_description: Fired when an XBlock is updated.
# .. event_data: XBlockData
XBLOCK_UPDATED = OpenEdxPublicSignal(
    event_type="org.openedx.content_authoring.xblock.updated.v1",
    data={
        "xblock_info": XBlockData,
    }
)

# .. event_type: org.openedx.content_authoring.xblock.published.v1
# .. event_name: XBLOCK_PUBLISHED
# .. event_key_field: xblock_info.usage_key
# .. event_description: Fired when an XBlock is published. If a parent block
#       with changes in one or more child blocks is published, only a single
#       XBLOCK_PUBLISHED event is fired with parent block details.
#       For example: If a section is published with changes in multiple units,
#       only a single event is fired with section details like :
#       `XBlockData(usage_key="section-usage-key", block_type="chapter")`
# .. event_data: XBlockData
XBLOCK_PUBLISHED = OpenEdxPublicSignal(
    event_type="org.openedx.content_authoring.xblock.published.v1",
    data={
        "xblock_info": XBlockData,
    }
)


# .. event_type: org.openedx.content_authoring.xblock.deleted.v1
# .. event_name: XBLOCK_DELETED
# .. event_key_field: xblock_info.usage_key
# .. event_description: Fired when an XBlock is deleted.
# .. event_data: XBlockData
XBLOCK_DELETED = OpenEdxPublicSignal(
    event_type="org.openedx.content_authoring.xblock.deleted.v1",
    data={
        "xblock_info": XBlockData,
    }
)


# .. event_type: org.openedx.content_authoring.xblock.duplicated.v1
# .. event_name: XBLOCK_DUPLICATED
# .. event_key_field: xblock_info.usage_key
# .. event_description: Fired when an XBlock is duplicated in Studio.
# .. event_data: DuplicatedXBlockData
XBLOCK_DUPLICATED = OpenEdxPublicSignal(
    event_type="org.openedx.content_authoring.xblock.duplicated.v1",
    data={
        "xblock_info": DuplicatedXBlockData,
    }
)


# .. event_type: org.openedx.content_authoring.course.certificate_config.changed.v1
# .. event_name: COURSE_CERTIFICATE_CONFIG_CHANGED
# .. event_description: Fired when a course certificate configuration changes in Studio.
#      Warning: This event is currently incompatible with the event bus, list/dict cannot be serialized yet
# .. event_data: CertificateConfigData
COURSE_CERTIFICATE_CONFIG_CHANGED = OpenEdxPublicSignal(
    event_type="org.openedx.content_authoring.course.certificate_config.changed.v1",
    data={
        "certificate_config": CertificateConfigData,
    }
)

# .. event_type: org.openedx.content_authoring.course.certificate_config.deleted.v1
# .. event_name: COURSE_CERTIFICATE_CONFIG_DELETED
# .. event_description: Fired when a course certificate configuration deletes in Studio.
#      Warning: This event is currently incompatible with the event bus, list/dict cannot be serialized yet
# .. event_data: CertificateConfigData
COURSE_CERTIFICATE_CONFIG_DELETED = OpenEdxPublicSignal(
    event_type="org.openedx.content_authoring.course.certificate_config.deleted.v1",
    data={
        "certificate_config": CertificateConfigData,
    }
)

# .. event_type: org.openedx.content_authoring.course.created.v1
# .. event_name: COURSE_CREATED
# .. event_description: emitted when a course is created
# .. event_data: CourseData
COURSE_CREATED = OpenEdxPublicSignal(
    event_type="org.openedx.content_authoring.course.created.v1",
    data={
        "course": CourseData,
    }
)

# .. event_type: org.openedx.content_authoring.content_library.created.v1
# .. event_name: CONTENT_LIBRARY_CREATED
# .. event_description: emitted when a content library is created
# .. event_data: ContentLibraryData
CONTENT_LIBRARY_CREATED = OpenEdxPublicSignal(
    event_type="org.openedx.content_authoring.content_library.created.v1",
    data={
        "content_library": ContentLibraryData,
    }
)

# .. event_type: org.openedx.content_authoring.content_library.updated.v1
# .. event_name: CONTENT_LIBRARY_UPDATED
# .. event_description: emitted when a content library is updated
# .. event_data: ContentLibraryData
CONTENT_LIBRARY_UPDATED = OpenEdxPublicSignal(
    event_type="org.openedx.content_authoring.content_library.updated.v1",
    data={
        "content_library": ContentLibraryData,
    }
)

# .. event_type: org.openedx.content_authoring.content_library.deleted.v1
# .. event_name: CONTENT_LIBRARY_DELETED
# .. event_description: emitted when a content library is deleted
# .. event_data: ContentLibraryData
CONTENT_LIBRARY_DELETED = OpenEdxPublicSignal(
    event_type="org.openedx.content_authoring.content_library.deleted.v1",
    data={
        "content_library": ContentLibraryData,
    }
)

# .. event_type: org.openedx.content_authoring.library_block.created.v1
# .. event_name: LIBRARY_BLOCK_CREATED
# .. event_description: emitted when a library block is created
# .. event_data: LibraryBlockData
LIBRARY_BLOCK_CREATED = OpenEdxPublicSignal(
    event_type="org.openedx.content_authoring.library_block.created.v1",
    data={
        "library_block": LibraryBlockData,
    }
)

# .. event_type: org.openedx.content_authoring.library_block.updated.v1
# .. event_name: LIBRARY_BLOCK_UPDATED
# .. event_description: emitted when a library block is updated
# .. event_data: LibraryBlockData
LIBRARY_BLOCK_UPDATED = OpenEdxPublicSignal(
    event_type="org.openedx.content_authoring.library_block.updated.v1",
    data={
        "library_block": LibraryBlockData,
    }
)

# .. event_type: org.openedx.content_authoring.library_block.deleted.v1
# .. event_name: LIBRARY_BLOCK_DELETED
# .. event_description: emitted when a library block is deleted
# .. event_data: LibraryBlockData
LIBRARY_BLOCK_DELETED = OpenEdxPublicSignal(
    event_type="org.openedx.content_authoring.library_block.deleted.v1",
    data={
        "library_block": LibraryBlockData,
    }
)

# .. event_type: org.openedx.content_authoring.content.object.tags.changed.v1
# .. event_name: CONTENT_OBJECT_TAGS_CHANGED
# .. event_description: emitted when an object's tags are changed
# .. event_data: ContentObjectData
CONTENT_OBJECT_TAGS_CHANGED = OpenEdxPublicSignal(
    event_type="org.openedx.content_authoring.content.object.tags.changed.v1",
    data={
        "content_object": ContentObjectData
    }
)

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
    ContentObjectChangedData,
    ContentObjectData,
    CourseCatalogData,
    CourseData,
    DuplicatedXBlockData,
    LibraryBlockData,
    LibraryCollectionData,
    XBlockData,
)
from openedx_events.tooling import OpenEdxPublicSignal

# .. event_type: org.openedx.content_authoring.course.catalog_info.changed.v1
# .. event_name: COURSE_CATALOG_INFO_CHANGED
# .. event_key_field: catalog_info.course_key
# .. event_description: Fired when a course changes in Studio in a way that is relevant for catalog consumers.
# .. event_data: CourseCatalogData
# .. event_trigger_repository: openedx/edx-platform
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
# .. event_trigger_repository: openedx/edx-platform
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
# .. event_trigger_repository: openedx/edx-platform
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
# .. event_trigger_repository: openedx/edx-platform
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
# .. event_trigger_repository: openedx/edx-platform
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
# .. event_trigger_repository: openedx/edx-platform
XBLOCK_DUPLICATED = OpenEdxPublicSignal(
    event_type="org.openedx.content_authoring.xblock.duplicated.v1",
    data={
        "xblock_info": DuplicatedXBlockData,
    }
)


# .. event_type: org.openedx.content_authoring.course.certificate_config.changed.v1
# .. event_name: COURSE_CERTIFICATE_CONFIG_CHANGED
# .. event_description: Fired when a course certificate configuration changes in Studio.
# .. event_data: CertificateConfigData
# .. event_warning: This event is not being currently used in any of the Open edX services. Review
#      https://github.com/openedx/openedx-events/issues/445 for more information about the future of this event.
COURSE_CERTIFICATE_CONFIG_CHANGED = OpenEdxPublicSignal(
    event_type="org.openedx.content_authoring.course.certificate_config.changed.v1",
    data={
        "certificate_config": CertificateConfigData,
    }
)

# .. event_type: org.openedx.content_authoring.course.certificate_config.deleted.v1
# .. event_name: COURSE_CERTIFICATE_CONFIG_DELETED
# .. event_description: Fired when a course certificate configuration deletes in Studio.
# .. event_data: CertificateConfigData
# .. event_warning: This event is not being currently used in any of the Open edX services. Review
#      https://github.com/openedx/openedx-events/issues/445 for more information about the future of this event.
COURSE_CERTIFICATE_CONFIG_DELETED = OpenEdxPublicSignal(
    event_type="org.openedx.content_authoring.course.certificate_config.deleted.v1",
    data={
        "certificate_config": CertificateConfigData,
    }
)

# .. event_type: org.openedx.content_authoring.course.created.v1
# .. event_name: COURSE_CREATED
# .. event_description: Emitted when a course is created.
# .. event_data: CourseData
# .. event_trigger_repository: openedx/edx-platform
COURSE_CREATED = OpenEdxPublicSignal(
    event_type="org.openedx.content_authoring.course.created.v1",
    data={
        "course": CourseData,
    }
)

# .. event_type: org.openedx.content_authoring.content_library.created.v1
# .. event_name: CONTENT_LIBRARY_CREATED
# .. event_description: Emitted when a content library is created.
# .. event_data: ContentLibraryData
# .. event_trigger_repository: openedx/edx-platform
CONTENT_LIBRARY_CREATED = OpenEdxPublicSignal(
    event_type="org.openedx.content_authoring.content_library.created.v1",
    data={
        "content_library": ContentLibraryData,
    }
)

# .. event_type: org.openedx.content_authoring.content_library.updated.v1
# .. event_name: CONTENT_LIBRARY_UPDATED
# .. event_description: Emitted when a content library is updated.
# .. event_data: ContentLibraryData
# .. event_trigger_repository: openedx/edx-platform
CONTENT_LIBRARY_UPDATED = OpenEdxPublicSignal(
    event_type="org.openedx.content_authoring.content_library.updated.v1",
    data={
        "content_library": ContentLibraryData,
    }
)

# .. event_type: org.openedx.content_authoring.content_library.deleted.v1
# .. event_name: CONTENT_LIBRARY_DELETED
# .. event_description: Emitted when a content library is deleted.
# .. event_data: ContentLibraryData
# .. event_trigger_repository: openedx/edx-platform
CONTENT_LIBRARY_DELETED = OpenEdxPublicSignal(
    event_type="org.openedx.content_authoring.content_library.deleted.v1",
    data={
        "content_library": ContentLibraryData,
    }
)

# .. event_type: org.openedx.content_authoring.library_block.created.v1
# .. event_name: LIBRARY_BLOCK_CREATED
# .. event_description: Emitted when a library block is created.
# .. event_data: LibraryBlockData
# .. event_trigger_repository: openedx/edx-platform
LIBRARY_BLOCK_CREATED = OpenEdxPublicSignal(
    event_type="org.openedx.content_authoring.library_block.created.v1",
    data={
        "library_block": LibraryBlockData,
    }
)

# .. event_type: org.openedx.content_authoring.library_block.updated.v1
# .. event_name: LIBRARY_BLOCK_UPDATED
# .. event_description: Emitted when a library block is updated.
# .. event_data: LibraryBlockData
# .. event_trigger_repository: openedx/edx-platform
LIBRARY_BLOCK_UPDATED = OpenEdxPublicSignal(
    event_type="org.openedx.content_authoring.library_block.updated.v1",
    data={
        "library_block": LibraryBlockData,
    }
)

# .. event_type: org.openedx.content_authoring.library_block.deleted.v1
# .. event_name: LIBRARY_BLOCK_DELETED
# .. event_description: Emitted when a library block is deleted.
# .. event_data: LibraryBlockData
# .. event_trigger_repository: openedx/edx-platform
LIBRARY_BLOCK_DELETED = OpenEdxPublicSignal(
    event_type="org.openedx.content_authoring.library_block.deleted.v1",
    data={
        "library_block": LibraryBlockData,
    }
)

# .. event_type: org.openedx.content_authoring.content.object.associations.changed.v1
# .. event_name: CONTENT_OBJECT_ASSOCIATIONS_CHANGED
# .. event_description: Emitted when an object's associations are changed, e.g tags, collections
# .. event_data: ContentObjectChangedData
# .. event_trigger_repository: openedx/edx-platform
CONTENT_OBJECT_ASSOCIATIONS_CHANGED = OpenEdxPublicSignal(
    event_type="org.openedx.content_authoring.content.object.associations.changed.v1",
    data={
        "content_object": ContentObjectChangedData
    }
)

# .. event_type: org.openedx.content_authoring.content.object.tags.changed.v1
# .. event_name: CONTENT_OBJECT_TAGS_CHANGED
# .. event_description: Emitted when an object's tags are changed.
# .. event_data: ContentObjectData
# .. event_warning: **DEPRECATED** please use CONTENT_OBJECT_ASSOCIATIONS_CHANGED instead.
CONTENT_OBJECT_TAGS_CHANGED = OpenEdxPublicSignal(
    event_type="org.openedx.content_authoring.content.object.tags.changed.v1",
    data={
        "content_object": ContentObjectData
    }
)

# .. event_type: org.openedx.content_authoring.content_library.collection.created.v1
# .. event_name: LIBRARY_COLLECTION_CREATED
# .. event_description: Emitted when a content library collection is created.
# .. event_data: LibraryCollectionData
# .. event_trigger_repository: openedx/edx-platform
LIBRARY_COLLECTION_CREATED = OpenEdxPublicSignal(
    event_type="org.openedx.content_authoring.content_library.collection.created.v1",
    data={
        "library_collection": LibraryCollectionData
    }
)

# .. event_type: org.openedx.content_authoring.content_library.collection.updated.v1
# .. event_name: LIBRARY_COLLECTION_UPDATED
# .. event_description: Emitted when when a content library collection is updated.
# .. event_data: LibraryCollectionData
# .. event_trigger_repository: openedx/edx-platform
LIBRARY_COLLECTION_UPDATED = OpenEdxPublicSignal(
    event_type="org.openedx.content_authoring.content_library.collection.updated.v1",
    data={
        "library_collection": LibraryCollectionData
    }
)

# .. event_type: org.openedx.content_authoring.content_library.collection.deleted.v1
# .. event_name: LIBRARY_COLLECTION_DELETED
# .. event_description: Emitted when an when a content library collection is deleted.
# .. event_data: LibraryCollectionData
# .. event_trigger_repository: openedx/edx-platform
LIBRARY_COLLECTION_DELETED = OpenEdxPublicSignal(
    event_type="org.openedx.content_authoring.content_library.collection.deleted.v1",
    data={
        "library_collection": LibraryCollectionData
    }
)

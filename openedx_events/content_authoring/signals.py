"""
Standardized signals definitions for events within the architecture subdomain ``content_authoring``.

All signals defined in this module must follow the name and versioning
conventions specified in OEP-41.

They also must comply with the payload definition specified in
docs/decisions/0003-events-payload.rst
"""

from openedx_events.content_authoring.data import (
    CertificateConfigData,
    CourseCatalogData,
    DuplicatedXBlockData,
    XBlockData,
)
from openedx_events.tooling import OpenEdxPublicSignal

# .. event_type: org.openedx.content_authoring.course.catalog_info.changed.v1
# .. event_name: COURSE_CATALOG_INFO_CHANGED
# .. event_description: Fired when a course changes in Studio in a way that is relevant for catalog consumers.
# .. event_data: CourseCatalogData
COURSE_CATALOG_INFO_CHANGED = OpenEdxPublicSignal(
    event_type="org.openedx.content_authoring.course.catalog_info.changed.v1",
    data={
        "catalog_info": CourseCatalogData,
    }
)


# .. event_type: org.openedx.content_authoring.xblock.published.v1
# .. event_name: XBLOCK_PUBLISHED
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

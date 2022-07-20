"""
Signal definitions for events within the architecture subdomain ``content_authoring``.

All signals defined in this module must follow the name and versioning
conventions specified in OEP-41.

They also must comply with the payload definition specified in
docs/decisions/0003-events-payload.rst
"""

from openedx_events.content_authoring.data import CourseCatalogData
from openedx_events.tooling import OpenEdxPublicSignal

# .. event_type: org.openedx.content_authoring.course.catalog_info.changed.v1
# .. event_name: COURSE_CATALOG_INFO_CHANGED
# .. event_description: Fired when a course changes in Studio in a way that is relevant for Catalog consumers.
# .. event_data: CourseCatalogData
COURSE_CATALOG_INFO_CHANGED = OpenEdxPublicSignal(
    event_type="org.openedx.content_authoring.course.catalog_info.changed.v1",
    data={
        "catalog_info": CourseCatalogData,
    }
)

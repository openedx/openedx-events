"""
Standardized signals definitions for events within the architecture subdomain ``analytics``.

All signals defined in this module must follow the name and versioning
conventions specified in OEP-41.

They also must comply with the payload definition specified in
docs/decisions/0003-events-payload.rst
"""

from openedx_events.analytics.data import TrackingLogData
from openedx_events.tooling import OpenEdxPublicSignal

# .. event_type: org.openedx.analytics.tracking.event.emitted.v1
# .. event_name: TRACKING_EVENT_EMITTED
# .. event_description: emitted when a tracking log is created.
# .. event_data: TrackingLogData
TRACKING_EVENT_EMITTED = OpenEdxPublicSignal(
    event_type="org.openedx.analytics.tracking.event.emitted.v1",
    data={
        "tracking_log": TrackingLogData,
    }
)

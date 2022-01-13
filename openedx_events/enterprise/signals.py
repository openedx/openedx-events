"""
Custom signals definitions that representing the Open edX platform events.

All signals defined in this module must follow the name and versioning
conventions specified in docs/decisions/0002-events-naming-and-versioning.rst

They also must comply with the payload definition specified in
docs/decisions/0003-events-payload.rst
"""

from openedx_events.enterprise.data import TrackingEvent
from openedx_events.tooling import OpenEdxPublicSignal

# .. event_type: org.openedx.enterprise.subscription.license.modified.v1
# .. event_name: LICENSE_MODIFIED
# .. event_description: mitted when a subscriptions.License record's data is modified.
# .. event_data: TrackingEvent
LICENSE_MODIFIED = OpenEdxPublicSignal(
    event_type="org.openedx.enterprise.subscription.license.modified.v1",
    data={
        "user": TrackingEvent,
    }
)

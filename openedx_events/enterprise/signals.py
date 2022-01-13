"""
Custom signals definitions that representing the Open edX platform events.

All signals defined in this module must follow the name and versioning
conventions specified in docs/decisions/0002-events-naming-and-versioning.rst

They also must comply with the payload definition specified in
docs/decisions/0003-events-payload.rst
"""

from openedx_events.enterprise.data import LicenseLifecycle
from openedx_events.tooling import OpenEdxPublicSignal

# .. event_type: org.openedx.enterprise.subscription.license.modified.v1
# .. event_name: LICENSE_CREATED
# .. event_description: emitted with Subscription.License is created.
# .. event_data: LicenseLifecycle
LICENSE_CREATED = OpenEdxPublicSignal(
    event_type="org.openedx.enterprise.subscription.license.created.v1",
    data={
        "lifecycle": LicenseLifecycle,
    }
)

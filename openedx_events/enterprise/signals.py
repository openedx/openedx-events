"""
Custom signals definitions that representing the Open edX platform events.

All signals defined in this module must follow the name and versioning
conventions specified in docs/decisions/0002-events-naming-and-versioning.rst

They also must comply with the payload definition specified in
docs/decisions/0003-events-payload.rst
"""

from openedx_events.enterprise.data import SubscriptionLicenseData
from openedx_events.tooling import OpenEdxPublicSignal

# .. event_type: org.openedx.enterprise.subscription.license.modified.v1
# .. event_name: LICENSE_MODIFIED
# .. event_description: emitted when a Subscription License is modified,
#     where "modified" means created, updated, revoked, etc.
#     WARNING: This event is being used for event bus prototype purposes and
#          should not be used, and should not be copied as a fully vetted pattern.
#     TODO(EventBus): Delete or make production ready post-prototype phase.
#           We will be splitting different actions into their own events (for created,
#           updated, revoked, etc.)
#           See: https://openedx.atlassian.net/browse/ARCHBOM-2008 for more details.
# .. event_data: SubscriptionLicenseData
SUBSCRIPTION_LICENSE_MODIFIED = OpenEdxPublicSignal(
    event_type="org.openedx.enterprise.subscription.license.modified.v0",
    data={
        "license": SubscriptionLicenseData,
    }
)

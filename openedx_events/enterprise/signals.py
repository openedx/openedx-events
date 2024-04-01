"""
Standardized signals definitions for events within the architecture subdomain ``enterprise``.

All signals defined in this module must follow the name and versioning
conventions specified in OEP-41.

They also must comply with the payload definition specified in
docs/decisions/0003-events-payload.rst
"""

from openedx_events.enterprise.data import SubsidyRedemption
from openedx_events.tooling import OpenEdxPublicSignal

# .. event_type: org.openedx.enterprise.subsidy.redeemed.v1
# .. event_name: SUBSIDY_REDEEMED
# .. event_description: emitted when an enterprise subsidy is utilized.
# .. event_data: SubsidyRedemption
SUBSIDY_REDEEMED = OpenEdxPublicSignal(
    event_type="org.openedx.enterprise.subsidy.redeemed.v1",
    data={
        "redemption": SubsidyRedemption,
    }
)

# .. event_type: org.openedx.enterprise.subsidy.redemption-reversed.v1
# .. event_name: SUBSIDY_REDEMPTION_REVERSED
# .. event_description: emitted when an enterprise subsidy is reversed.
# .. event_data: SubsidyRedemption
SUBSIDY_REDEMPTION_REVERSED = OpenEdxPublicSignal(
    event_type="org.openedx.enterprise.subsidy.redemption-reversed.v1",
    data={
        "redemption": SubsidyRedemption,
    }
)

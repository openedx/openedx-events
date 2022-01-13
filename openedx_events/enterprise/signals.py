"""
Custom signals definitions that representing the Open edX platform events.

All signals defined in this module must follow the name and versioning
conventions specified in docs/decisions/0002-events-naming-and-versioning.rst

They also must comply with the payload definition specified in
docs/decisions/0003-events-payload.rst
"""

from openedx_events.enterprise.data import TrackingEvent
from openedx_events.tooling import OpenEdxPublicSignal

# .. event_type: org.openedx.learning.student.registration.completed.v1
# .. event_name: STUDENT_REGISTRATION_COMPLETED
# .. event_description: emitted when the user registration process in the LMS is completed.
# .. event_data: UserData
LICENSE_MODIFIED = OpenEdxPublicSignal(
    event_type="org.openedx.enterprise.subscription.license.modified.v1",
    data={
        "user": TrackingEvent,
    }
)

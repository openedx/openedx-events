"""
Standard Open edX events related to the Open edX authorization framework.

This module defines signals that are used to notify other parts of the system
about changes or actions related to authorization.
"""

from openedx_events.authz.data import RoleAssignmentData
from openedx_events.tooling import OpenEdxPublicSignal

# .. event_type: org.openedx.authz.role_assignment.created
# .. event_name: ROLE_ASSIGNMENT_CREATED
# .. event_key_field: user.pii.username
# .. event_description: Emitted when a role assignment is created in Open edX.
# .. event_data: RoleAssignmentData
# .. event_trigger_repository: openedx/openedx-authz
ROLE_ASSIGNMENT_CREATED = OpenEdxPublicSignal(
    event_type="org.openedx.authz.role_assignment.created",
    data={
        "role_assignment": RoleAssignmentData,
    }
)


# .. event_type: org.openedx.authz.role_assignment.deleted
# .. event_name: ROLE_ASSIGNMENT_DELETED
# .. event_key_field: user.pii.username
# .. event_description: Emitted when a role assignment is deleted in Open edX.
# .. event_data: RoleAssignmentData
# .. event_trigger_repository: openedx/openedx-authz
ROLE_ASSIGNMENT_DELETED = OpenEdxPublicSignal(
    event_type="org.openedx.authz.role_assignment.deleted",
    data={
        "role_assignment": RoleAssignmentData,
    }
)

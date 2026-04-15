"""Data attributes for events related to the authorization framework."""

from typing import NamedTuple, Optional

import attr


@attr.s(frozen=True)
class RoleAssignmentData:
    """Data related to a specific role assignment.

    A role assignment represents the assignment of a role to a subject (e.g., user)
    within a specific scope (e.g., course, organization).

    Attributes:
        operation (str): The operation being performed. Use ``OPERATIONS.created`` or
            ``OPERATIONS.deleted``.
        subject (str): The subject to which the role is assigned (e.g., 'user^john_doe').
        role (str): The role that is assigned (e.g., 'course_admin').
        scope (str): The scope in which the role is assigned (e.g., 'course-v1:edX+DemoX+Demo_Course').
        actor (Optional[str]): Username of the user performing the operation.
            None if not known or not applicable (system-initiated actions).
    """

    class Operations(NamedTuple):
        created: str = "created"
        deleted: str = "deleted"

    OPERATIONS = Operations()

    operation: str = attr.ib(validator=attr.validators.in_(OPERATIONS))
    subject: str = attr.ib()
    role: str = attr.ib()
    scope: str = attr.ib()
    actor: Optional[str] = attr.ib(default=None)

"""Data attributes for events related to the authorization framework."""

import attr


@attr.s(frozen=True)
class RoleAssignmentData:
    """Data related to a specific role assignment.

    A role assignment represents the assignment of a role to a subject (e.g., user)
    within a specific scope (e.g., course, organization).

    Attributes:
        operation (str): The operation being performed (e.g., 'created', 'deleted').
        subject (str): The subject to which the role is assigned (e.g., 'user^john_doe').
        role (str): The role that is assigned (e.g., 'course_admin').
        scope (str): The scope in which the role is assigned (e.g., 'course-v1:edX+DemoX+Demo_Course').
        actor (str): Username of the user performing the operation.
            None if not known or not applicable (system-initiated actions).
    """

    operation = attr.ib(type=str)
    subject = attr.ib(type=str)
    role = attr.ib(type=str)
    scope = attr.ib(type=str)
    actor = attr.ib(type=str, default=None)

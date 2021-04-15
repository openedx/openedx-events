"""
openedx_hooks.signals.enrollment.v1 module.
"""

from django.dispatch import Signal

# Signal that fires when a user enrolls in a course
ENROLLMENT_USER = Signal(providing_args=["user", "enrollement", "is_new", "mode"])

# Signal that fires when a user unenrolls in a course
UNENROLLMENT_USER = Signal(providing_args=["user", "enrollement"])

"""
openedx_events.signals.auth.v1 module.
"""

from django.dispatch import Signal

# Signal that fires when a user register in the platform
REGISTER_USER = Signal(providing_args=["user", "registration"])

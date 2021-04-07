"""
openedx_events.signals.auth.v1 module.
"""

from django.dispatch import Signal

REGISTER_USER = Signal(providing_args=["user", "registration"])

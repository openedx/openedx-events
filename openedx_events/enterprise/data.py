"""
Data attributes for events within the architecture subdomain `enterprise`.

These attributes follow the form of attr objects specified in OEP-49 data
pattern.
"""
from datetime import datetime

import attr

@attr.s(frozen=True)
class TrackingEvent:
    """
    License events to be put on event bus
    TODO: figure out proper description
    """
    license_uuid = attr.ib(type=str)
    license_activation_key = attr.ib(type=str)
    previous_license_uuid = attr.ib(type=str)
    assigned_date = attr.ib(type=str)
    activation_date = attr.ib(type=str)
    assigned_lms_user_id = attr.ib(type=str)
    assigned_email = attr.ib(type=str)
    expiration_processed = attr.ib(type=bool)
    auto_applied = attr.ib(type=bool, default=False)
    enterprise_customer_uuid = attr.ib(type=str, default=None)
    enterprise_customer_slug = attr.ib(type=str, default=None)
    enterprise_customer_name = attr.ib(type=str, default=None)
    customer_agreement_uuid = attr.ib(type=str, default=None)

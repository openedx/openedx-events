"""
Data attributes for events within the architecture subdomain `enterprise`.

These attributes follow the form of attr objects specified in OEP-49 data
pattern.
"""
import attr


@attr.s(frozen=True)
class TrackingEvent:
    """
    License events to be put on event bus.

    TODO: figure out proper description

    Arguments:
        license_uuid (str):
        license_activation_key (str):
        previous_license_uuid (str):
        assigned_date (str):
        activation_date (str):
        assigned_lms_user_id (str):
        assigned_email (str):
        expiration_processed (bool):
        auto_applied (bool):
        enterprise_customer_uuid (str):
        enterprise_customer_slug (str):
        enterprise_customer_name (str):
        customer_agreement_uuid (str):
    """

    license_uuid = attr.ib(type=str)
    license_activation_key = attr.ib(type=str)
    previous_license_uuid = attr.ib(type=str)
    assigned_date = attr.ib(type=str)
    activation_date = attr.ib(type=str)
    assigned_email = attr.ib(type=str)
    expiration_processed = attr.ib(type=bool)
    assigned_lms_user_id = attr.ib(type=int, default=None)
    auto_applied = attr.ib(type=bool, default=False)
    enterprise_customer_uuid = attr.ib(type=str, default=None)
    enterprise_customer_slug = attr.ib(type=str, default=None)
    enterprise_customer_name = attr.ib(type=str, default=None)
    customer_agreement_uuid = attr.ib(type=str, default=None)

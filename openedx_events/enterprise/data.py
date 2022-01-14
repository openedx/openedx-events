"""
Data attributes for events within the architecture subdomain `enterprise`.

These attributes follow the form of attr objects specified in OEP-49 data
pattern.
"""
import attr


@attr.s(frozen=True)
class SubscriptionLicenseData:
    """
    Attributes defined for Open edX Subscription License object.

    Arguments:
        license_uuid (str): The UUID linked to this license and storing in the License Manager DB.
                            This value is always present.
        license_activation_key (str):
        previous_license_uuid (str): The UUID linked to the previous license that this license is
                                     a renewal for. Non-empty only on after the
                                     edx.server.license-manager.license-lifecycle.renewed event has occurred.
        assigned_date (str): Formatted ISO-8601 Date String representing the date
                             this license was most recently assigned to the assigned_email.
                             May be empty.
        activation_date (str): Formatted ISO-8601 Date String this license was most recently activated
                               for the assigned_email.
                               May be empty.
        assigned_lms_user_id (str): The LMS User id of the user that this license 'belongs to'.
                                    May be empty if this license is not activated yet.
        assigned_email (str): The email assigned to this license.
                              Will be empty if this license is not assigned to a learner yet.
        expiration_processed (bool): Boolean value of License 'expiration_processed' field, may be True or False.
                                     True means a license is expired.
        auto_applied (bool):
        enterprise_customer_uuid (str): UUID used to internally represent an enterprise
        enterprise_customer_slug (str): Short name of an enterprise used in the URLs and other places
                                        for display purposes.
        enterprise_customer_name (str): Long Name of an enterprise customer. Used for display and reporting
        customer_agreement_uuid (str): The active Customer Agreement UUID that this license is linked to.
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

"""
Data attributes for events within the architecture subdomain ``enterprise``.

These attributes follow the form of attr objects specified in OEP-49 data
pattern.
"""

import attr


@attr.s(frozen=True)
class SubsidyRedemption:
    """
    Attributes for a Subsidy Redemption object.

    Arguments:
        subsidy_identifier (str): unique identifier to fetch the applied subsidy
        content_key (str): content id where subsidy is utilized
        lms_user_id (str): lms user id of subsidy beneficiary
    """

    subsidy_identifier = attr.ib(type=str)
    content_key = attr.ib(type=str)
    lms_user_id = attr.ib(type=int)

"""
Data attributes for events within the architecture subdomain ``enterprise``.

These attributes follow the form of attr objects specified in OEP-49 data
pattern.
"""
from datetime import datetime
from uuid import UUID

import attr
from opaque_keys.edx.keys import CourseKey


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


@attr.s(frozen=True)
class BaseLedgerTransaction:
    """
    Defines the common attributes of the transaction classes below.
    """

    uuid = attr.ib(type=UUID)
    created = attr.ib(type=datetime)
    modified = attr.ib(type=datetime)
    idempotency_key = attr.ib(type=str)
    quantity = attr.ib(type=int)
    state = attr.ib(type=str)


@attr.s(frozen=True)
class LedgerTransactionReversal(BaseLedgerTransaction):
    """
    Attributes of an ``openedx_ledger.Reversal`` record.

    A ``Reversal`` is a model that represents the "undo-ing" of a ``Transaction`` (see below). It's primarily
    used within the domain of edX Enterprise for recording unenrollments and refunds of subsidized
    enterprise enrollments.
    https://github.com/openedx/openedx-ledger/blob/master/openedx_ledger/models.py

    Arguments:
        uuid (str): Primary identifier of the record.
        created (datetime): When the record was created.
        modified (datetime): When the record was last modified.
        idempotency_key (str): Client-generated unique value to achieve idempotency of operations.
        quantity (int): How many units of value this reversal represents (e.g. USD cents).
        state (str): Current lifecyle state of the record, one of (created, pending, committed, failed).
    """


@attr.s(frozen=True)
class LedgerTransaction(BaseLedgerTransaction):
    """
    Attributes of an ``openedx_ledger.Transaction`` record.

    A ``Transaction`` is a model that represents value moving in or out of a ``Ledger``. It's primarily
    used within the domain of edX Enterprise for recording the redemption of subsidized enrollments.
    https://github.com/openedx/openedx-ledger/blob/master/openedx_ledger/models.py

    Arguments:
        uuid (UUID): Primary identifier of the Transaction.
        created (datetime): When the record was created.
        modified (datetime): When the record was last modified.
        idempotency_key (str): Client-generated unique value to achieve idempotency of operations.
        quantity (int): How many units of value this transaction represents (e.g. USD cents).
        state (str): Current lifecyle state of the record, one of (created, pending, committed, failed).
        ledger_uuid (UUID): The primary identifier of this Transaction's ledger object.
        subsidy_access_policy_uuid (UUID): The primary identifier of the subsidy access policy for this transaction.
        lms_user_id (int): The LMS user id of the user associated with this transaction.
        content_key (CourseKey): The course (run) key associated with this transaction.
        parent_content_key (str): The parent (just course, not run) key for the course key.
        fulfillment_identifier (str): The identifier of the subsidized enrollment record for a learner,
          generated durning enrollment.
        reversal (LedgerTransactionReversal): Any reversal associated with this transaction.
    """

    ledger_uuid = attr.ib(type=UUID)
    subsidy_access_policy_uuid = attr.ib(type=UUID)
    lms_user_id = attr.ib(type=int)
    content_key = attr.ib(type=CourseKey)
    parent_content_key = attr.ib(type=str, default=None)
    fulfillment_identifier = attr.ib(type=str, default=None)
    reversal = attr.ib(type=LedgerTransactionReversal, default=None)

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
    Data related to a Subsidy Redemption object.

    Attributes:
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
    Data related to a Ledger Transaction object.

    Attributes:
        uuid (UUID): Primary identifier of the record.
        created (datetime): When the record was created.
        modified (datetime): When the record was last modified.
        idempotency_key (str): Client-generated unique value to achieve idempotency of operations.
        quantity (int): How many units of value this transaction represents (e.g. USD cents).
        state (str): Current lifecyle state of the record, one of (created, pending, committed, failed).
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

    Attributes:
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

    Attributes:
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


@attr.s(frozen=True)
class EnterpriseCustomerUser:
    """
    Data related to an Enterprise Customer User object.

    Django model definition: https://github.com/openedx/edx-enterprise/blob/cc873d6/enterprise/models.py#L1036

    Attributes:
        id (int): Primary identifier of the record.
        created (datetime): When the record was created.
        modified (datetime): When the record was last modified.
        enterprise_customer_uuid (UUID): The enterprise customer to which the user is linked.
        user_id (int): The LMS user ID corresponding to this enterprise user.
        active (bool): The active enterprise user for the given LMS user.
        linked (bool): This enterprise user has been linked to an enterprise customer.
        is_relinkable (bool): When set to False, the user cannot be relinked to the enterprise.
        invite_key (UUID): Invite key used to link a learner to an enterprise.
        should_inactivate_other_customers (bool): When enabled along with `active`, all other linked enterprise
           customers for this user will be marked as inactive upon save.
    """

    id = attr.ib(type=int)
    created = attr.ib(type=datetime)
    modified = attr.ib(type=datetime)
    enterprise_customer_uuid = attr.ib(type=UUID)
    user_id = attr.ib(type=int)
    active = attr.ib(type=bool)
    linked = attr.ib(type=bool)
    is_relinkable = attr.ib(type=bool)
    should_inactivate_other_customers = attr.ib(type=bool)
    invite_key = attr.ib(type=UUID, default=None)


@attr.s(frozen=True)
class EnterpriseCourseEnrollment:
    """
    Data related to an Enterprise Course Enrollment object.

    Django model definition: https://github.com/openedx/edx-enterprise/blob/cc873d6/enterprise/models.py#L1983

    Attributes:
        id (int): Primary identifier of the record.
        created (datetime): When the record was created.
        modified (datetime): When the record was last modified.
        enterprise_customer_user (EnterpriseCustomerUser): The enterprise learner to which this enrollment is attached.
        course_id (CourseKey): The ID of the course in which the learner was enrolled.
        saved_for_later (bool): Specifies whether a user marked this course as saved for later in the learner portal.
        source_slug (str): DB slug for the source of the enrollment, e.g. "enrollment_task", "management_command", etc.
        unenrolled (bool): Specifies whether the related LMS course enrollment object was unenrolled.
        unenrolled_at (datetime): Specifies when the related LMS course enrollment object was unenrolled.
    """

    id = attr.ib(type=int)
    created = attr.ib(type=datetime)
    modified = attr.ib(type=datetime)
    enterprise_customer_user = attr.ib(type=EnterpriseCustomerUser)
    course_id = attr.ib(type=CourseKey)
    saved_for_later = attr.ib(type=bool)
    source_slug = attr.ib(type=str, default=None)
    unenrolled = attr.ib(type=bool, default=None)
    unenrolled_at = attr.ib(type=datetime, default=None)


@attr.s(frozen=True)
class BaseEnterpriseFulfillment:
    """
    Defines the common attributes of enterprise fulfillment classes, i.e. ``enterprise.EnterpriseFulfillmentSource``.

    Django model definition: https://github.com/openedx/edx-enterprise/blob/cc873d6/enterprise/models.py#L2213

    Attributes:
        uuid (str): Primary identifier of the record.
        created (datetime): When the record was created.
        modified (datetime): When the record was last modified.
        fulfillment_type (str): Subsidy fulfillment type, typical values: "license", "learner_credit", "coupon_code".
        enterprise_course_entitlement_uuid (UUID): The course entitlement the associated subsidy is for.
        enterprise_course_enrollment (EnterpriseCourseEnrollment): The course enrollment the associated subsidy is
           for.
        is_revoked (bool): Whether the enterprise subsidy is revoked, e.g., when a user's license is revoked.
    """

    uuid = attr.ib(type=UUID)
    created = attr.ib(type=datetime)
    modified = attr.ib(type=datetime)
    fulfillment_type = attr.ib(type=str)
    is_revoked = attr.ib(type=bool)
    enterprise_course_entitlement_uuid = attr.ib(type=UUID, default=None)
    enterprise_course_enrollment = attr.ib(type=EnterpriseCourseEnrollment, default=None)


@attr.s(frozen=True)
class LearnerCreditEnterpriseCourseEnrollment(BaseEnterpriseFulfillment):
    """
    Attributes of an ``enterprise.LearnerCreditEnterpriseCourseEnrollment`` record.

    Django model definition: https://github.com/openedx/edx-enterprise/blob/cc873d6/enterprise/models.py#L2325

    All of the same attributes from BaseEnterpriseFulfillment plus the following:

    Attributes:
        transaction_id (UUID): Ledgered transaction UUID to associate with this learner credit fulfillment.
    """

    transaction_id = attr.ib(type=UUID, default=None)


@attr.s(frozen=True)
class LicensedEnterpriseCourseEnrollment(BaseEnterpriseFulfillment):
    """
    Attributes of an ``enterprise.LicensedEnterpriseCourseEnrollment`` record.

    Django model definition: https://github.com/openedx/edx-enterprise/blob/cc873d6/enterprise/models.py#L2355

    All of the same attributes from BaseEnterpriseFulfillment plus the following:

    Attributes:
        license_uuid (UUID): License UUID to associate with this enterprise license fulfillment.
    """

    license_uuid = attr.ib(type=UUID, default=None)


@attr.s(frozen=True)
class EnterpriseGroup:
    """
    Attributes of an ``enterprise.EnterpriseGroup`` record.

    Django model definition:
    https://github.com/openedx/edx-enterprise/blob/4ae2831a02087747da7bee7ea5cdd1d22929a059/enterprise/models.py#L4701

    Arguments:
        uuid (UUID): Primary identifier of the record.
    """

    uuid = attr.ib(type=UUID)

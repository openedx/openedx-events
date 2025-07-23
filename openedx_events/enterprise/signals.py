"""
Standardized signals definitions for events within the architecture subdomain ``enterprise``.

All signals defined in this module must follow the name and versioning
conventions specified in OEP-41.

They also must comply with the payload definition specified in
docs/decisions/0003-events-payload.rst
"""

from openedx_events.enterprise.data import (
    EnterpriseGroup,
    LearnerCreditEnterpriseCourseEnrollment,
    LedgerTransaction,
    SubsidyRedemption,
)
from openedx_events.tooling import OpenEdxPublicSignal

# .. event_type: org.openedx.enterprise.subsidy.redeemed.v1
# .. event_name: SUBSIDY_REDEEMED
# .. event_description: emitted when an enterprise subsidy is utilized.
# .. event_data: SubsidyRedemption
# .. event_warning: This event is not being currently used in any of the Open edX services. Review
#      https://github.com/openedx/openedx-events/issues/445 for more information about the future of this event.
SUBSIDY_REDEEMED = OpenEdxPublicSignal(
    event_type="org.openedx.enterprise.subsidy.redeemed.v1",
    data={
        "redemption": SubsidyRedemption,
    }
)

# .. event_type: org.openedx.enterprise.subsidy.redemption-reversed.v1
# .. event_name: SUBSIDY_REDEMPTION_REVERSED
# .. event_description: emitted when an enterprise subsidy is reversed.
# .. event_data: SubsidyRedemption
# .. event_warning: This event is not being currently used in any of the Open edX services. Review
#      https://github.com/openedx/openedx-events/issues/445 for more information about the future of this event.
SUBSIDY_REDEMPTION_REVERSED = OpenEdxPublicSignal(
    event_type="org.openedx.enterprise.subsidy.redemption-reversed.v1",
    data={
        "redemption": SubsidyRedemption,
    }
)


# .. event_type: org.openedx.enterprise.subsidy_ledger_transaction.created.v1
# .. event_name: LEDGER_TRANSACTION_CREATED
# .. event_description: emitted when an enterprise ledger transaction is created.
#      See: https://github.com/openedx/openedx-ledger/tree/main/docs/decisions
# .. event_data: LedgerTransaction
# .. event_trigger_repository: openedx/enterprise-subsidy
LEDGER_TRANSACTION_CREATED = OpenEdxPublicSignal(
    event_type="org.openedx.enterprise.subsidy_ledger_transaction.created.v1",
    data={
        "ledger_transaction": LedgerTransaction,
    }
)


# .. event_type: org.openedx.enterprise.subsidy_ledger_transaction.committed.v1
# .. event_name: LEDGER_TRANSACTION_COMMITTED
# .. event_description: emitted when an enterprise ledger transaction is committed.
#      See: https://github.com/openedx/openedx-ledger/tree/main/docs/decisions
# .. event_data: LedgerTransaction
# .. event_trigger_repository: openedx/enterprise-subsidy
LEDGER_TRANSACTION_COMMITTED = OpenEdxPublicSignal(
    event_type="org.openedx.enterprise.subsidy_ledger_transaction.committed.v1",
    data={
        "ledger_transaction": LedgerTransaction,
    }
)


# .. event_type: org.openedx.enterprise.subsidy_ledger_transaction.failed.v1
# .. event_name: LEDGER_TRANSACTION_FAILED
# .. event_description: emitted when an enterprise ledger transaction fails.
#      See: https://github.com/openedx/openedx-ledger/tree/main/docs/decisions
# .. event_data: LedgerTransaction
# .. event_trigger_repository: openedx/enterprise-subsidy
LEDGER_TRANSACTION_FAILED = OpenEdxPublicSignal(
    event_type="org.openedx.enterprise.subsidy_ledger_transaction.failed.v1",
    data={
        "ledger_transaction": LedgerTransaction,
    }
)


# .. event_type: org.openedx.enterprise.subsidy_ledger_transaction.reversed.v1
# .. event_name: LEDGER_TRANSACTION_REVERSED
# .. event_description: emitted when an enterprise ledger transaction is reversed.
#      See: https://github.com/openedx/openedx-ledger/tree/main/docs/decisions
# .. event_data: LedgerTransaction
# .. event_trigger_repository: openedx/enterprise-subsidy
LEDGER_TRANSACTION_REVERSED = OpenEdxPublicSignal(
    event_type="org.openedx.enterprise.subsidy_ledger_transaction.reversed.v1",
    data={
        "ledger_transaction": LedgerTransaction,
    }
)


# .. event_type: org.openedx.enterprise.learner_credit_course_enrollment.revoked.v1
# .. event_name: LEARNER_CREDIT_COURSE_ENROLLMENT_REVOKED
# .. event_description: emitted when a LearnerCreditEnterpriseCourseEnrollment is revoked. This most often happens when
#      an enterprise learner unenrolls from a course which was LC-subsidized.
# .. event_data: LearnerCreditEnterpriseCourseEnrollment
# .. event_trigger_repository: openedx/edx-enterprise
LEARNER_CREDIT_COURSE_ENROLLMENT_REVOKED = OpenEdxPublicSignal(
    event_type="org.openedx.enterprise.learner_credit_course_enrollment.revoked.v1",
    data={
        "learner_credit_course_enrollment": LearnerCreditEnterpriseCourseEnrollment,
    }
)


"""
To test this event in LMS, you can use the following command:
`python3 manage.py lms produce_event --signal openedx_events.enterprise.signals.ENTERPRISE_GROUP_DELETED \
--topic enterprise-core --key-field enterprise_group.uuid \
--data '{"enterprise_group": { "uuid": "d509a63b-eb11-4dc8-8b84-4688c7335110" }}'`
"""
# .. event_type: org.openedx.enterprise.enterprise_group.deleted.v1
# .. event_name: ENTERPRISE_GROUP_DELETED
# .. event_description: emitted when an EnterpriseGroup is deleted.
# .. event_data: EnterpriseGroup
# .. event_trigger_repository: openedx/edx-enterprise
ENTERPRISE_GROUP_DELETED = OpenEdxPublicSignal(
    event_type="org.openedx.enterprise.enterprise_group.deleted.v1",
    data={
        "enterprise_group": EnterpriseGroup,
    }
)

"""
Standardized signals definitions for events within the architecture subdomain ``enterprise``.

All signals defined in this module must follow the name and versioning
conventions specified in OEP-41.

They also must comply with the payload definition specified in
docs/decisions/0003-events-payload.rst
"""

from openedx_events.enterprise.data import LedgerTransaction, SubsidyRedemption
from openedx_events.tooling import OpenEdxPublicSignal

# .. event_type: org.openedx.enterprise.subsidy.redeemed.v1
# .. event_name: SUBSIDY_REDEEMED
# .. event_description: emitted when an enterprise subsidy is utilized.
# .. event_data: SubsidyRedemption
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
LEDGER_TRANSACTION_REVERSED = OpenEdxPublicSignal(
    event_type="org.openedx.enterprise.subsidy_ledger_transaction.reversed.v1",
    data={
        "ledger_transaction": LedgerTransaction,
    }
)

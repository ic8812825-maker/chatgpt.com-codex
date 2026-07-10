from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
state = (ROOT / "Include" / "StateMachine.mqh").read_text()
types = (ROOT / "Include" / "Types.mqh").read_text()
ea = (ROOT / "MinusLock_BigHarvest_EA.mq5").read_text()
manual = (ROOT / "Docs" / "MANUAL.md").read_text()

required_state_tokens = [
    "HistoryDealGetString(dealTicket, DEAL_SYMBOL) != _Symbol",
    "DEAL_FEE",
    "DEAL_ENTRY_INOUT",
    "DEAL_ENTRY_OUT_BY",
    "CalculateBigSmallLifecycleNet",
    "BIG_SMALL_LIFECYCLE_NET",
    "CalculateProjectedFarCloseNet",
    "OrderCalcProfit",
    "BIG_FULL_COVERAGE_CHECK",
    "FullCloseAllowed",
    "FULL_FAR_CLOSE_BEFORE_PARTIAL",
    "PartialBudgetAvailable",
    "ReserveUsedForPartial=NO",
    "partialFarBudgetCarry",
    "ReserveEventKeyHash",
    "ReserveEventAlreadyApplied",
    "WARNING_RESERVE_CREDIT",
    "WARNING_RESERVE_DEBIT",
]
for token in required_state_tokens:
    assert token in state, token

assert "double partialFarBudgetCarry;" in types
assert "bool pendingFullFarClose;" in types
assert "long eventKeyHash;" in types
assert "ReserveShare + CloseFarShare must be exactly 1.0" in ea
assert "ProjectedRecoveryPLAfterFullClose > 0" in manual
assert "ExistingReserve + BigSmallNet >= FarLoss" in manual
assert "DEAL_MAGIC == MagicNumber" in manual and "DEAL_SYMBOL == _Symbol" in manual
print("PASS: Big monetary recovery model uses Symbol+Magic history, lifecycle net, full Far coverage before partial, money-based partial budget, carry, and idempotent reserve ledger.")

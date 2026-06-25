from pathlib import Path
root = Path(__file__).resolve().parents[1]
state = (root / "Include" / "StateMachine.mqh").read_text()
recalc = state.split("bool RecalculateRealCycleStatsFromHistory()", 1)[1].split("double GetClosedProfitForPosition", 1)[0]
assert "HistorySelect(fromTime, toTime)" in recalc
assert "Ctx.cycleStartTime" in recalc
assert "INITIAL_BUY" in recalc and "INITIAL_SELL" in recalc
assert "REAL_RECOVERY_SKIP_INITIAL_LOCK" in recalc
calc = state.split("double CalcRealRecoveryPL()", 1)[1].split("bool RecalculateRealCycleStatsFromHistory()", 1)[0]
assert "initialIgnoredProfit" not in calc
ledger = state.split("double RebuildReserveFromLedger()", 1)[1].split("bool ValidateNoOrphanManagedPositions", 1)[0]
assert "initialIgnoredProfit" not in ledger
print("INITIAL_IGNORED_PROFIT_EXCLUDED_CHECK PASS")

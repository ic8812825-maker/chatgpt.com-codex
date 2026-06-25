from pathlib import Path
logger = (Path(__file__).resolve().parents[1] / "Include" / "Logger.mqh").read_text()
for token in [
    '"InitialDeposit"', '"InitialIgnoredProfit"', '"CycleStartBalance"', '"CurrentBalance"',
    '"AccountPL"', '"RecoveryPL"', '"PassByAccountPL"', '"PassByRecoveryPL"',
    '"RealClosedProfit"', '"RealClosedLoss"', '"RealSwap"', '"RealCommission"',
    '"LastSystemCloseComment"', '"LastCloseWasSystemClose"', '"FinalCloseType"',
]:
    assert token in logger, token
assert "currentBalance - cycleStartBalance" in logger
assert "currentBalance - initialDeposit" in logger
print("CSV_RECOVERY_FIELDS_CHECK PASS")

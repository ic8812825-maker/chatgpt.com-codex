from pathlib import Path
state = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text()
assert "BIG_FULL_COVERAGE_CHECK" in state
assert "coverageAvailable >= farCloseLoss + SafetyBufferMoney" in state
assert "projectedRecoveryPLAfterFullClose >= MinimumRecoveryProfitMoney" in state
assert state.index("BIG_FULL_COVERAGE_CHECK") < state.index("BIG_PARTIAL_FAR")
print("PASS: Big full Far close is checked before partial Far.")

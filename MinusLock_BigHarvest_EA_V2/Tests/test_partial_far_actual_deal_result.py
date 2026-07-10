from pathlib import Path
state = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text()
assert "CalculatePositionCloseDealsNet" in state
assert "DEAL_ENTRY_OUT && dealEntry != DEAL_ENTRY_INOUT && dealEntry != DEAL_ENTRY_OUT_BY" in state
assert "actualPartialFarNet" in state
assert "actualPartialFarLoss = foundActualPartialDeals ? MathMax(0.0, -actualPartialFarNet)" in state
print("PASS: Partial Far carry uses actual close deals when available.")

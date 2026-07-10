from pathlib import Path
root=Path(__file__).resolve().parents[1]
config=(root/"Include"/"Config.mqh").read_text()
state=(root/"Include"/"StateMachine.mqh").read_text()
assert "input double MinimumRecoveryProfitMoney" in config
assert "input double SafetyBufferMoney" in config
assert "input double EstimatedCloseCommissionPerLot" in config
assert "result.estimatedCommission = closeLot * EstimatedCloseCommissionPerLot" in state
assert "result.projectedNet = profit + swapPart - result.estimatedCommission - SafetyBufferMoney" in state
print("PASS: Far close projection includes commission estimate and safety buffer.")

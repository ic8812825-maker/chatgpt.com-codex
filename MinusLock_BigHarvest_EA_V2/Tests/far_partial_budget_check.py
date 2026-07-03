from pathlib import Path
root = Path(__file__).resolve().parents[1]
state = (root / 'Include' / 'StateMachine.mqh').read_text()
recovery = (root / 'Include' / 'RecoveryMath.mqh').read_text()
assert 'CalcCloseFarLotRaw(Ctx.pendingCloseFarBudget, Ctx.effectiveFarDistancePoints)' in state
assert 'ClosePositionByTicket(Ctx.farTicket, Ctx.pendingCloseFarLot)' in state
assert 'return closeFarBudget / lossPerLot;' in recovery
assert 'NormalizeLotDown(rawLot)' in recovery
assert 'if(rounded > farLot)' in recovery
assert 'CloseFarActualCost' in state
print('FAR_PARTIAL_BUDGET_CHECK PASS')

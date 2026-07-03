from pathlib import Path
root = Path(__file__).resolve().parents[1]
state = (root / 'Include' / 'StateMachine.mqh').read_text()
recovery = (root / 'Include' / 'RecoveryMath.mqh').read_text()
audit = (root / 'Docs' / 'BIG_SCENARIO_ENGINEERING_AUDIT.md').read_text()
assert 'Ctx.pendingReserveAdd = realBigHarvestNet * WorkReserveShare;' in state
assert 'Ctx.pendingCloseFarBudget = realBigHarvestNet * WorkCloseFarShare;' in state
assert 'return netProfit * WorkCloseFarShare;' in recovery
assert 'return netProfit * WorkReserveShare;' in recovery
assert 'WorkCloseFarShare + WorkReserveShare' in audit
assert 'realBigHarvestNet = realClosedBigProfit + realClosedSmallProfit;' in state
assert 'FAIL' in audit and 'realBigHarvestNet` includes Small net' in audit
print('BIG_PROFIT_SPLIT_CHECK PASS')

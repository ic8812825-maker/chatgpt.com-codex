from pathlib import Path
root = Path(__file__).resolve().parents[1]
state = (root / 'Include' / 'StateMachine.mqh').read_text()
recovery = (root / 'Include' / 'RecoveryMath.mqh').read_text()
audit = (root / 'Docs' / 'BIG_SCENARIO_ENGINEERING_AUDIT.md').read_text()
assert 'bigSmallNet = bigLifecycleNet + smallLifecycleNet;' in state
assert 'Ctx.pendingReserveAdd = bigSmallNet * WorkReserveShare;' in state
assert 'Ctx.pendingCloseFarBudget = bigSmallNet - Ctx.pendingReserveAdd;' in state
assert 'BIG_SCENARIO_NET BigLifecycleNet=' in state
assert 'return netProfit * WorkCloseFarShare;' in recovery
assert 'return netProfit * WorkReserveShare;' in recovery
assert 'CloseFarShare' in audit and 'ReserveShare' in audit
assert 'PASS: `BigScenarioNet = ClosedBigNet + ClosedSmallNet` is the approved model' in audit
assert ('FAIL:' + ' realBigHarvestNet includes ' + 'Small net') not in audit
print('BIG_PROFIT_SPLIT_CHECK PASS')

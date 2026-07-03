from pathlib import Path
root = Path(__file__).resolve().parents[1]
state = (root / 'Include' / 'StateMachine.mqh').read_text()
types = (root / 'Include' / 'Types.mqh').read_text()
for token in ['STATE_BIG_HARVEST_CLOSE_BIG', 'STATE_BIG_HARVEST_CLOSE_SMALL', 'STATE_BIG_HARVEST_CALC_NET', 'STATE_BIG_HARVEST_CLOSE_FAR', 'STATE_BIG_HARVEST_CHECK_FINAL']:
    assert token in types and token in state, token
for fn in ['ProcessBigHarvest()', 'ProcessBigHarvestCloseBig()', 'ProcessBigHarvestCloseSmall()', 'ProcessBigHarvestCalcNet()', 'ProcessBigHarvestCloseFar()', 'ProcessBigHarvestCheckFinal()']:
    assert f'void {fn}' in state, fn
for token in ['BIG_SCENARIO_START', 'BIG_CLOSED', 'BIG_NET_PROFIT', 'BIG_PROFIT_SPLIT', 'CLOSE_FAR_BUDGET', 'RESERVE_ADD', 'PARTIAL_FAR_CLOSE', 'FAR_REMAINING', 'RESERVE_AFTER', 'BIG_SCENARIO_END']:
    assert token in state, token
assert state.index('void ProcessBigHarvestCloseBig()') < state.index('void ProcessBigHarvestCloseSmall()') < state.index('void ProcessBigHarvestCalcNet()') < state.index('void ProcessBigHarvestCloseFar()') < state.index('void ProcessBigHarvestCheckFinal()')
print('BIG_SCENARIO_STATE_FLOW_CHECK PASS')

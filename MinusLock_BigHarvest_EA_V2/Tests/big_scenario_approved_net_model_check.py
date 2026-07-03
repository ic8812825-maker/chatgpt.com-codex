from pathlib import Path
root = Path(__file__).resolve().parents[1]
audit = (root / 'Docs' / 'BIG_SCENARIO_ENGINEERING_AUDIT.md').read_text()
state = (root / 'Include' / 'StateMachine.mqh').read_text()
logger = (root / 'Include' / 'Logger.mqh').read_text()
report = (root / 'Reports' / 'BigScenario_Trace_Report.md').read_text()
for text in [audit, report]:
    assert 'BigScenarioNet = ClosedBigNet + ClosedSmallNet' in text
assert 'Approved Big Scenario Net Model' in audit
assert ('FAIL:' + ' realBigHarvestNet includes ' + 'Small net') not in audit
assert ('Big' + 'NetProfit') not in audit
for token in ['BIG_SCENARIO_NET', 'ClosedBigNet', 'ClosedSmallNet', 'BigScenarioNet']:
    assert token in state, token
    assert token in logger or token == 'BIG_SCENARIO_NET', token
assert ('BIG_' + 'NET_PROFIT') not in state
assert ('Big' + 'NetProfit') not in logger
print('BIG_SCENARIO_APPROVED_NET_MODEL_CHECK PASS')

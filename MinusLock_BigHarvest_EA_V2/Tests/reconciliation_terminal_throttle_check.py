from pathlib import Path
text = Path('MinusLock_BigHarvest_EA_V2/Include/ReconciliationEngine.mqh').read_text()
config = Path('MinusLock_BigHarvest_EA_V2/Include/Config.mqh').read_text()
for token in ['LastTerminalReconLogTime', 'SuppressedTerminalReconCount', 'IsTerminalStateForReconciliationThrottle', 'ShouldThrottleTerminalReconciliation', 'TERMINAL_STATE_STABLE']:
    assert token in text
for state in ['STATE_STOP_MAX_LEVELS', 'STATE_CLOSED_PROFIT', 'STATE_CLOSED_RECOVERY_LOSS', 'STATE_REVERSE_LIMIT', 'STATE_ERROR']:
    assert state in text
assert 'TerminalStateLogIntervalSeconds' in config
assert 'if(ShouldThrottleTerminalReconciliation())' in text
print('RECONCILIATION_TERMINAL_THROTTLE_CHECK PASS')

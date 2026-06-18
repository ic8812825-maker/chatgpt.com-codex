#!/usr/bin/env python3
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
state = (ROOT / 'MinusLock_BigHarvest_EA/Include/StateMachine.mqh').read_text(encoding='utf-8')
main = (ROOT / 'MinusLock_BigHarvest_EA/MinusLock_BigHarvest_EA.mq5').read_text(encoding='utf-8')
for token in ['ValidateTerminalStateSafety', 'TerminalStateOpensPosition', 'TerminalStateRetriesOpen', 'PendingStateWithoutRetry', 'INIT_FAILED']:
    assert token in state or token in main, f'missing FSM safety token: {token}'
assert 'if(!ValidateTerminalStateSafety())' in main
print('terminal_state_safety_check PASS')

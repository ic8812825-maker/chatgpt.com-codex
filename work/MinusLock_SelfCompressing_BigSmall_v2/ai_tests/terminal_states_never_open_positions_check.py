#!/usr/bin/env python3
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parents[1]
state = (ROOT / 'MinusLock_BigHarvest_EA/Include/StateMachine.mqh').read_text(encoding='utf-8')
terminal_block = re.search(r'case STATE_CLOSED_PROFIT:(.*?)default:', state, re.S)
assert terminal_block, 'terminal block not found'
block = terminal_block.group(1)
for forbidden in ['RetryOpenNewBig()', 'RetryOpenNewSmall()', 'OpenPosition(', 'OpenBigSmall(']:
    assert forbidden not in block, f'terminal states contain forbidden open/retry call: {forbidden}'
assert 'case STATE_OPEN_NEW_BIG_PENDING:' in state and 'RetryOpenNewBig();' in state
assert 'case STATE_OPEN_NEW_SMALL_PENDING:' in state and 'RetryOpenNewSmall();' in state
print('terminal_states_never_open_positions_check PASS')

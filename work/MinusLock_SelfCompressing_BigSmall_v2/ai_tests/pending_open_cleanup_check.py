#!/usr/bin/env python3
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
text = (ROOT / 'MinusLock_BigHarvest_EA/Include/StateMachine.mqh').read_text(encoding='utf-8')
for token in ['void ClearPendingOpenContext()', 'Ctx.pendingLot = 0.0;', 'Ctx.pendingDirection = DIR_NONE;', 'Ctx.pendingComment = "";', 'Ctx.pendingAttempts = 0;', 'Ctx.pendingOperation = "";']:
    assert token in text, f'missing pending cleanup token: {token}'
for retry in ['RetryOpenNewBig', 'RetryOpenNewSmall']:
    idx = text.index(f'void {retry}()')
    chunk = text[idx:text.index('\n}', idx)+2]
    assert 'if(opened)' in chunk and 'ClearPendingOpenContext();' in chunk
print('pending_open_cleanup_check PASS')

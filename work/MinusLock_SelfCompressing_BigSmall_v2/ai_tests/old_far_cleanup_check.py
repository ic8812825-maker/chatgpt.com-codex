#!/usr/bin/env python3
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
text = (ROOT / 'MinusLock_BigHarvest_EA/Include/StateMachine.mqh').read_text(encoding='utf-8')
close = text.index('SMALL_AT_FAR_CLOSE_OLD_FAR')
for token in ['Ctx.oldFarTicket = oldFarTicket;', 'Ctx.oldFarLot = oldFarLot;', 'Ctx.oldFarDirection = oldFarDirection;', 'Ctx.oldFarOpenPrice = oldFarOpenPrice;']:
    assert token in text[close:], f'missing old-far save token: {token}'
for token in ['Ctx.farTicket = 0;', 'Ctx.farLot = 0.0;', 'Ctx.farDirection = DIR_NONE;', 'Ctx.farOpenPrice = 0.0;']:
    assert token in text[close:], f'missing active Far cleanup token: {token}'
print('old_far_cleanup_check PASS')

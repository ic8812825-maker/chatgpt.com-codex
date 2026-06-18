#!/usr/bin/env python3
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
text = (ROOT / 'MinusLock_BigHarvest_EA/Include/StateMachine.mqh').read_text(encoding='utf-8')
assert 'Ctx.savedSmallDirection = smallDirection;' in text
assert 'Ctx.savedSmallClosePrice = ExitPriceForDirection(smallDirection);' in text
assert 'double currentPrice = Ctx.savedSmallTouchPrice;' in text
save_idx = text.index('Ctx.savedSmallDirection = smallDirection;')
clear_idx = text.index('Ctx.smallDirection = DIR_NONE;', save_idx)
assert save_idx < clear_idx, 'small direction must be saved before smallDirection is cleared'
process = text[text.index('void ProcessSmallAtFarTouch()'):text.index('void StartSmallScenarioPhaseFSM()')]
assert 'double currentPrice = CurrentPriceForSmallTouch(Ctx.smallDirection);' not in process
print('saved_small_direction_check PASS')

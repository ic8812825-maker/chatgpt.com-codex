#!/usr/bin/env python3
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
text = (ROOT / 'MinusLock_BigHarvest_EA/Include/StateMachine.mqh').read_text(encoding='utf-8')
assert 'void StartBigHarvestPhaseFSM()' in text
assert 'void StartSmallScenarioPhaseFSM()' in text
assert 'case STATE_BIG_HARVEST:\n         StartBigHarvestPhaseFSM();' in text
assert 'case STATE_SMALL_SCENARIO:\n         StartSmallScenarioPhaseFSM();' in text
assert 'void ProcessBigHarvest()' not in text
assert 'void ProcessSmallScenario()' not in text
print('phase_wrapper_rename_check PASS')

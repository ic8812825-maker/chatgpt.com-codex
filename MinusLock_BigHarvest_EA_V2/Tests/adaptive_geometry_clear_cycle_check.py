from pathlib import Path
root = Path(__file__).resolve().parents[1]
geom = (root / 'Include' / 'GeometryEngine.mqh').read_text()
state = (root / 'Include' / 'StateMachine.mqh').read_text()
for token in ['bool CanClearCycleGeometry()', 'void ClearCycleGeometry()', 'CLEAR_CYCLE_GEOMETRY_SKIPPED', 'ACTIVE_CONTEXT_OR_POSITIONS']:
    assert token in geom, token
for token in ['Ctx.cycleATRPoints = 0.0', 'Ctx.workInitialTriggerPoints = 0', 'Ctx.workBigMoveStartPoints = 0', 'Ctx.workBigMoveStepPoints = 0', 'Ctx.workFarDistancePoints = 0', 'Ctx.geometryModeUsed = (int)GEOMETRY_MANUAL', 'Ctx.geometryCalculatedTime = 0']:
    assert token in geom, token
assert 'ClearCycleGeometry();' in state.split('void ResetRecoveryContext()', 1)[1].split('double CalcRealRecoveryPL', 1)[0]
terminal_block = state.split('case STATE_CLOSED_PROFIT:', 1)[1].split('case STATE_STOP_MAX_LEVELS:', 1)[0]
assert 'ClearCycleGeometry();' in terminal_block
print('ADAPTIVE_GEOMETRY_CLEAR_CYCLE_CHECK PASS')

from pathlib import Path
root = Path(__file__).resolve().parents[1]
geom = (root / 'Include' / 'GeometryEngine.mqh').read_text()
state = (root / 'Include' / 'StateMachine.mqh').read_text()
for token in ['bool CanClearCycleGeometry()', 'void ClearCycleGeometry(bool persist = false, int clearReasonCode = GEOMETRY_CLEAR_RESET_CONTEXT)', 'CLEAR_CYCLE_GEOMETRY_SKIPPED', 'ACTIVE_CONTEXT_OR_POSITIONS']:
    assert token in geom, token
for token in ['Ctx.cycleATRPoints = 0.0', 'Ctx.workInitialTriggerPoints = 0', 'Ctx.workBigMoveStartPoints = 0', 'Ctx.workBigMoveStepPoints = 0', 'Ctx.workFarDistancePoints = 0', 'Ctx.geometryModeUsed = (int)GEOMETRY_MANUAL', 'Ctx.geometryCalculatedTime = 0', 'Ctx.geometryCleared = 0', 'Ctx.geometryClearReasonCode = GEOMETRY_CLEAR_NONE']:
    assert token in geom, token
assert 'ClearCycleGeometry(false, GEOMETRY_CLEAR_RESET_CONTEXT);' in state.split('void ResetRecoveryContext()', 1)[1].split('double CalcRealRecoveryPL', 1)[0]
terminal_block = state.split('case STATE_CLOSED_PROFIT:', 1)[1].split('case STATE_UNCLOSED_CYCLE:', 1)[0]
assert 'ClearCycleGeometry(true, GEOMETRY_CLEAR_CLOSED_PROFIT);' in terminal_block
assert 'ClearCycleGeometry(true, GEOMETRY_CLEAR_CLOSED_RECOVERY_LOSS);' in terminal_block
assert 'ClearCycleGeometry(true, GEOMETRY_CLEAR_STOP_MAX_LEVELS);' in terminal_block
print('ADAPTIVE_GEOMETRY_CLEAR_CYCLE_CHECK PASS')

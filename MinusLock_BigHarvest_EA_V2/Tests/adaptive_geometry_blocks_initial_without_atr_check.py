from pathlib import Path
root = Path(__file__).resolve().parents[1]
geom = (root / 'Include' / 'GeometryEngine.mqh').read_text()
state = (root / 'Include' / 'StateMachine.mqh').read_text()
for token in ['EnsureGeometryReadyForInitialLock()', 'INITIAL_LOCK_BLOCKED_ATR_NOT_READY', 'INITIAL_LOCK_ALLOWED_ATR_READY']:
    assert token in geom, token
assert 'if(!EnsureGeometryReadyForInitialLock())\n      return;' in state
print('ADAPTIVE_GEOMETRY_BLOCKS_INITIAL_WITHOUT_ATR_CHECK PASS')

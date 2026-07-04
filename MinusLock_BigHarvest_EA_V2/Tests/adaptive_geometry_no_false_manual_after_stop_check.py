from pathlib import Path
root = Path(__file__).resolve().parents[1]
geom = (root / 'Include' / 'GeometryEngine.mqh').read_text()
state = (root / 'Include' / 'StateMachine.mqh').read_text()
logger = (root / 'Include' / 'Logger.mqh').read_text()
assert 'case STATE_STOP_MAX_LEVELS:' in state
assert 'ClearCycleGeometry(true, GEOMETRY_CLEAR_STOP_MAX_LEVELS);' in state
for text in [geom, logger, state]:
    assert 'GeometryMode=MANUAL ATRPoints=0.0' not in text
assert 'return "NO_ACTIVE_CYCLE";' in geom
assert 'GEOMETRY_SOURCE_CLEARED' in geom and 'GeometrySource=", GeometrySourceForDiagnostics()' in geom
assert 'STATE_STOP_MAX_LEVELS' in geom
print('ADAPTIVE_GEOMETRY_NO_FALSE_MANUAL_AFTER_STOP_CHECK PASS')

from pathlib import Path
root = Path(__file__).resolve().parents[1]
geom = (root / 'Include' / 'GeometryEngine.mqh').read_text()
state = (root / 'Include' / 'StateMachine.mqh').read_text()
types = (root / 'Include' / 'Types.mqh').read_text()
for token in ['enum GeometryClearReasonEnum', 'GEOMETRY_CLEAR_STOP_MAX_LEVELS', 'GeometryClearReasonToString', 'CLEAR_CYCLE_GEOMETRY_DONE', 'PreviousRuntimeGeometryMode', 'PreviousATRPoints', 'PreviousWorkInitial', 'ClearReason=']:
    assert token in geom, token
for token in ['int geometryCleared', 'int geometryClearReasonCode']:
    assert token in types, token
assert 'ClearCycleGeometry(true, GEOMETRY_CLEAR_STOP_MAX_LEVELS);' in state
assert 'GeometryCleared' in state and 'GeometryClearReasonCode' in state
print('ADAPTIVE_GEOMETRY_CLEAR_REASON_CHECK PASS')

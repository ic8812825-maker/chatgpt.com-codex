from pathlib import Path
root = Path(__file__).resolve().parents[1]
state = (root / 'Include' / 'StateMachine.mqh').read_text()
block = state.split('void LogReconciliationContextSummary', 1)[1].split('bool HasOpenLegContext', 1)[0]
for token in ['ConfiguredGeometryMode=%s', 'RuntimeGeometryMode=%s', 'GeometrySource=%s', 'GeometryActive=%s', 'GeometryCleared=%s', 'GeometryClearReason=%s', 'WorkSource=%s', 'FallbackReason=%s']:
    assert token in block, token
assert 'GeometryMode=%s ATRPoints=%.1f' not in block
assert 'MANUAL_FALLBACK_FOR_DISPLAY_ONLY' in block
print('ADAPTIVE_GEOMETRY_RECONCILIATION_SUMMARY_CHECK PASS')

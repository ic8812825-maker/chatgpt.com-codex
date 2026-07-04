from pathlib import Path
root = Path(__file__).resolve().parents[1]
geom = (root / 'Include' / 'GeometryEngine.mqh').read_text()
panel = geom.split('void UpdateGeometryPanel()', 1)[1].split('bool CanClearCycleGeometry()', 1)[0]
for token in ['Configured:', 'Runtime:', 'Source:', 'ATRPoints=', 'WorkInitial=', 'WorkBigStart=', 'WorkBigStep=', 'WorkFar=', 'FallbackReason=', 'ClearReason=', 'GeometryActive=', 'GeometryReady=', 'TradingBlocked=', 'ATRIndicator=', 'GeometryCleared=']:
    assert token in panel, token
assert 'DisplayWorkInitialTriggerPoints()' in panel
assert 'EnsureCycleGeometry' not in panel
print('ADAPTIVE_GEOMETRY_COMMENT_PANEL_CHECK PASS')

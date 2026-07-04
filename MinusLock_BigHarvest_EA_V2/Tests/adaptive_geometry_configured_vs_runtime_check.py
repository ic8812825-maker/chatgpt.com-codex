from pathlib import Path
root = Path(__file__).resolve().parents[1]
geom = (root / 'Include' / 'GeometryEngine.mqh').read_text()
logger = (root / 'Include' / 'Logger.mqh').read_text()
for token in ['ConfiguredGeometryModeToString()', 'RuntimeGeometryModeToString()', 'ConfiguredGeometryMode', 'RuntimeGeometryMode', 'GeometrySourceForDiagnostics()']:
    assert token in geom or token in logger, token
for token in ['GEOMETRY_ATR_SAFE', 'GEOMETRY_ATR_BALANCED', 'GEOMETRY_ATR_PROFIT', 'GEOMETRY_ATR_CUSTOM']:
    assert token in geom, token
assert 'GeometryModeToString(GeometryModeEnum mode)' in geom
assert 'return "GEOMETRY_ATR_SAFE";' in geom
assert '"ConfiguredGeometryMode", "RuntimeGeometryMode"' in logger
print('ADAPTIVE_GEOMETRY_CONFIGURED_VS_RUNTIME_CHECK PASS')

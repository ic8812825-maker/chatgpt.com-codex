from pathlib import Path
root = Path(__file__).resolve().parents[1]
config = (root / 'Include' / 'Config.mqh').read_text()
geom = (root / 'Include' / 'GeometryEngine.mqh').read_text()
assert 'input bool AllowATRManualFallback = false;' in config
assert 'if(IsATRGeometryMode() && !AllowATRManualFallback)' in geom
assert 'TradingAllowedByFallback=YES' in geom
assert 'UseManualGeometryFallback(reason, reasonCode);' in geom
print('ADAPTIVE_GEOMETRY_NO_AUTO_MANUAL_FALLBACK_CHECK PASS')

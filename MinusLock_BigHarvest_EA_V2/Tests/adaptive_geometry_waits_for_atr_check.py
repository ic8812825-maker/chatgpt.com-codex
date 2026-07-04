from pathlib import Path
root = Path(__file__).resolve().parents[1]
geom = (root / 'Include' / 'GeometryEngine.mqh').read_text()
for token in ['ATR_GEOMETRY_WAITING', 'RuntimeGeometryMode=WAITING_ATR', 'GeometrySource=ATR_NOT_READY', 'TradingBlocked=YES', 'MarkATRGeometryWaiting']:
    assert token in geom, token
assert 'if(IsATRGeometryMode() && !AllowATRManualFallback)' in geom
print('ADAPTIVE_GEOMETRY_WAITS_FOR_ATR_CHECK PASS')
